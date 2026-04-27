"""文档结构识别：章节切分、子段 marker、表标题。两个 extractor 共用。

设计原则：
- **单源化**所有"识别哪一行算 marker / 算表标题"的正则。历史上两个 extractor
  各维护一份导致漂移：4.4.2 的 `SMN板响应参数` 前缀两边都吃过亏；4.2.39 的
  `响应参数 1` 数字前空格只有 examples 兼容、tables 漏抓。统一后两边行为
  一致，再出 doc bug 只需要在这里改一处。
- **容错为先**：marker / 表标题正则在文档作者排版手滑时尽量识别，让漏抓
  在 diff 阶段集中暴露，而不是在 extractor 阶段静默失败。
"""
from __future__ import annotations

import re

# =================== 章节标题 ===================

# "4.2.39 创建SP服务的OS安装配置" 形式的章节首行。
HEADING_RE = re.compile(r"^(\d+(?:\.\d+)+)[\s\t]+([^\s/{][^/{}]{0,80})$")
_TRAILING_PAGENO = re.compile(r"(\d{1,4})$")


def _strip_trailing_pageno(title: str) -> str:
    """剥掉标题末尾被 docx→txt 转换附加的页码（仅当页码紧跟非数字字符）。"""
    m = _TRAILING_PAGENO.search(title)
    if m and m.start() > 0 and not title[m.start() - 1].isdigit():
        return title[: m.start()]
    return title


# =================== 子段 marker ===================

SECTION_MARKERS: tuple[str, ...] = (
    "接口功能", "接口约束", "调用方法", "URI",
    "请求参数", "请求示例", "响应参数", "响应示例",
    "返回值", "样例",
)
# 一行被识别为 marker 的三种写法（命中后归到不带前缀/数字的基础 marker）：
#   "响应参数"               基础写法
#   "响应参数1" / "响应参数 1" / "请求示例 2"
#       ↑ \s*\d* 兼容数字前空格（4.2.39 多组示例 "请求示例 1/2/3"）
#   "SMN板响应参数" / "业务板响应参数"
#       ↑ \S{1,5}板 兼容板型短前缀（4.4.2 区分 SMN板 / 业务板 两套响应表）
# 前缀强制以"板"结尾，避免 "本接口请求参数" 之类正文句子被误判。
_MARKER_RE = re.compile(
    r"^(?:\S{1,5}板)?("
    + "|".join(re.escape(m) for m in SECTION_MARKERS)
    + r")\s*\d*$"
)


def match_marker(stripped: str) -> str | None:
    """识别 stripped 行是否是子段 marker；命中返回基础 marker，否则 None。"""
    m = _MARKER_RE.match(stripped)
    return m.group(1) if m else None


# =================== 表标题 ===================

# "表X-XXX Path参数列表" / "表X-XXX Response参数列表" / "Path参数列表"。
# 三种写法都是 iter_tables 用来识别"新表开始"的强匹配。
_TABLE_TITLE_RE = re.compile(
    r"^(?:表\s*[\d\-.]+\s+)?(?:Path|Header|Body|Query|Response)?参数列表\s*$"
)
# 任何 "表X-YYY <文字>" 形式——不要求"参数列表"结尾。
# 用作 iter_tables 的硬停止条件：遇到下一张表就断开，不管它是不是参数列表。
# 修 4.4.7：表4-712 "支持自定义调速的刀片列表" 之前会被吃进上一张 Body 表，
# 刀片型号 (TS200-2280, X6800, ...) 误抓为 body 参数。
_ANY_TABLE_HEADER_RE = re.compile(r"^表\s*[\d\-.]+\s+\S")


def is_table_title(s: str) -> bool:
    """是否是"参数列表"形式的表标题（iter_tables 用来识别新表的开头）。"""
    return bool(_TABLE_TITLE_RE.match(s))


# =================== 通用辅助 ===================

# "返回状态码为200：xxx" / "返回状态码为500: xxx"——出现在表与表之间的散文，
# iter_tables 把它当成表的边界。
STATUS_CODE_PROSE_RE = re.compile(r"^返回状态码为\d+")


def split_columns(line: str) -> list[str]:
    """按 tab 或 ≥2 个空格切列；空列被丢掉。"""
    return [c for c in re.split(r"\t+|  +", line.strip()) if c != ""]


# =================== 章节切分 ===================

def split_sections(text: str) -> list[dict]:
    """按 HEADING_RE 把全文切成章节列表，每个 dict = {number, title, lines}。"""
    sections: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        stripped = line.strip()
        match = HEADING_RE.match(stripped)
        if match:
            if current is not None:
                sections.append(current)
            current = {
                "number": match.group(1),
                "title": _strip_trailing_pageno(match.group(2).strip()),
                "lines": [],
            }
            continue
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        sections.append(current)
    return sections


def section_has_uri(sec: dict) -> bool:
    """判断 section 是否是接口小节——lines 里存在独立的 'URI' 行。"""
    return any(line.strip() == "URI" for line in sec["lines"])


def dedup_sections(sections: list[dict]) -> list[dict]:
    """按 (number, title) 去重：带 URI 标记的优先；否则保留较后出现的一条。"""
    best: dict[tuple[str, str], int] = {}
    for i, sec in enumerate(sections):
        key = (sec["number"], sec["title"])
        prev = best.get(key)
        if prev is None:
            best[key] = i
            continue
        prev_has = section_has_uri(sections[prev])
        cur_has = section_has_uri(sec)
        if cur_has and not prev_has:
            best[key] = i
        elif cur_has == prev_has:
            best[key] = i
    keep = set(best.values())
    return [s for i, s in enumerate(sections) if i in keep]


# =================== 子段切分 ===================

def split_subsections(lines: list[str]) -> dict[str, list[str]]:
    """把章节内 lines 按 marker 切成 {marker: [lines, ...]}。

    所有已知 marker（SECTION_MARKERS）都会出现在结果 dict 里（默认空 list），
    调用方 .get()/直接索引都安全。
    """
    subs: dict[str, list[str]] = {m: [] for m in SECTION_MARKERS}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        marker = match_marker(stripped)
        if marker is not None:
            current = marker
            continue
        if current is not None:
            subs[current].append(line)
    return subs


# =================== 表切分 ===================

def iter_tables(lines: list[str]):
    """从一段 lines 里依次产出 (title, body_lines) 表对。

    停止条件（任一命中就把当前表收口）：
      - 下一张"参数列表"表          (_TABLE_TITLE_RE)
      - 任何 "表X-YYY ..." 形式标题  (_ANY_TABLE_HEADER_RE) ← 4.4.7 修复
      - 下一个子段 marker            (SECTION_MARKERS 精确成员)
      - 章节标题                    (HEADING_RE)
      - "返回状态码为..." 散文        (STATUS_CODE_PROSE_RE)
    """
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not is_table_title(s):
            i += 1
            continue
        title = s
        j = i + 1
        body: list[str] = []
        while j < n:
            tt = lines[j].strip()
            if is_table_title(tt):
                break
            if _ANY_TABLE_HEADER_RE.match(tt):
                break
            if tt in SECTION_MARKERS:
                break
            if HEADING_RE.match(tt):
                break
            if STATUS_CODE_PROSE_RE.match(tt):
                break
            body.append(lines[j])
            j += 1
        yield title, body
        i = j
