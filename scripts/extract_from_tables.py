#!/usr/bin/env python3
"""
从 PoDManager 接口文档 (.docx 或 .txt) 中逐个接口提取 URI 与参数名。

每个接口只抽取"表格第一列"的参数名（即参数名称），按 path/header/body/query/response 分类：

    interfaces:
      - section: "4.2.25"
        title:   "导出日志信息"
        method:  POST
        uri:     /redfish/v1/Managers/{manager_id}/...
        params:
          path:     [manager_id, logservices_id]
          header:   [X-Auth-Token, Content-Type]
          body:     [Type, Content]
          query:    []
          response: ["@odata.context", "@odata.type", ...]

用法：
    python3 extract_from_tables.py                             # 使用默认输入
    python3 extract_from_tables.py <输入文件> [输出yaml]

    默认输入：<仓库根>/data/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx
    默认输出：
      - <仓库根>/output/<输入文件名>.interfaces.yaml  （结构化）
      - <仓库根>/output/<输入文件名>.uris.txt         （每行 "[METHOD] URI"，顺序与 yaml 一致）

依赖：仅 Python 3 标准库；若安装了 PyYAML 则用 YAML 输出，否则自动回退 JSON。
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402


# =================== 数据结构 ===================

@dataclass
class Params:
    path: list[str] = field(default_factory=list)
    header: list[str] = field(default_factory=list)
    body: list[str] = field(default_factory=list)
    query: list[str] = field(default_factory=list)
    response: list[str] = field(default_factory=list)


@dataclass
class Interface:
    section: str
    title: str
    method: str
    uri: str
    params: Params


# =================== 章节与小节切分 ===================

HEADING_RE = re.compile(r"^(\d+(?:\.\d+)+)[\s\t]+([^\s/{][^/{}]{0,80})$")
_TRAILING_PAGENO = re.compile(r"(\d{1,4})$")


def _strip_trailing_pageno(title: str) -> str:
    m = _TRAILING_PAGENO.search(title)
    if m and m.start() > 0 and not title[m.start() - 1].isdigit():
        return title[: m.start()]
    return title

SECTION_MARKERS = (
    "接口功能", "接口约束", "调用方法", "URI",
    "请求参数", "请求示例", "响应参数", "响应示例",
    "返回值", "样例",
)
# 兼容带数字后缀的 marker，如 "响应示例1"/"响应示例2"/"请求示例1"。
# 命中时把内容归到不带数字的基础 marker。
_MARKER_WITH_SUFFIX_RE = re.compile(
    r"^(" + "|".join(re.escape(m) for m in SECTION_MARKERS) + r")\d*$"
)


def split_sections(text: str) -> list[dict]:
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


def _section_has_uri(sec: dict) -> bool:
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
        prev_has = _section_has_uri(sections[prev])
        cur_has = _section_has_uri(sec)
        if cur_has and not prev_has:
            best[key] = i
        elif cur_has == prev_has:
            best[key] = i
    keep = set(best.values())
    return [s for i, s in enumerate(sections) if i in keep]


def split_subsections(lines: list[str]) -> dict[str, list[str]]:
    subs: dict[str, list[str]] = {m: [] for m in SECTION_MARKERS}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        m = _MARKER_WITH_SUFFIX_RE.match(stripped)
        if m:
            current = m.group(1)  # 去掉尾部数字后缀，归到基础 marker
            continue
        if current is not None:
            subs[current].append(line)
    return subs


# =================== 表格解析（仅为了取"参数名称"首列） ===================

REQUIRED_VALUES = {"是", "否", "必选", "可选"}
# 白名单由 scripts/type_enum.py 扫描全文档"类型"列的真实取值，按出现次数 ≥2 的
# 合法类型词归入而成。
TYPE_VALUES = {
    # --- 英文 ---
    "string", "int", "integer", "uint", "bool", "boolean", "array", "object",
    "float", "number", "null", "list", "dict", "enum", "long", "short",
    "double", "map", "byte", "timestamp",
    "String",  # 大写首字母变体
    "URI",     # Redfish 把 URI 当类型用
    "array[object]", "array[string]",  # 带方括号的数组语法
    # --- 中文基础类型 ---
    "字符串", "字符", "字符型",
    "数字", "整数", "整型", "长整型", "短整型",
    "布尔", "布尔值", "布尔型",
    "浮点", "浮点数", "浮点型", "小数",
    "枚举", "枚举型",
    "数组", "列表", "对象", "字典", "集合", "映射",
    "自定义属性", "属性",
    "日期", "时间", "时间戳", "字节",
    # --- 文档里把类名当类型用的情况 ---
    "用户", "角色", "权限", "权限集合",
    # --- 联合/特殊写法 ---
    "null或字符串",
    # --- "-" 与 en-dash "–"：类型列留空用 "-" 占位（真实文档 350+43 次）---
    "-", "–",
}
# "整型/字符型/浮点型" 等以 型 结尾的变体统一兜底；
# "xx列表/xx数组/xx对象/xx集合/xx属性/xx字典/xx映射" 类 domain-specific 类型也归这里
TYPE_SUFFIX_RE = re.compile(r"^.{0,10}(列表|数组|对象|集合|属性|字典|映射|型)$")
STATUS_CODE_PROSE_RE = re.compile(r"^返回状态码为\d+")


def split_columns(line: str) -> list[str]:
    return [c for c in re.split(r"\t+|  +", line.strip()) if c != ""]


def looks_like_type(s: str) -> bool:
    if not s:
        return False
    if s in REQUIRED_VALUES or s in TYPE_VALUES:
        return True
    return bool(TYPE_SUFFIX_RE.match(s))


def is_new_row(cols: list[str]) -> bool:
    """新行的第 2~3 列应当是"是/否"或类型词。"""
    if len(cols) < 2:
        return False
    for i in range(1, min(4, len(cols))):
        if looks_like_type(cols[i]):
            return True
    return False


# 参数名长相：ASCII 字母/@/_ 开头，只含 ASCII 字母数字和 _ @ . - /
# 用于两个地方：①过滤非标识符首列（避免"文件传输协议包括：sftp"被 "-" 触发成新行）
#              ②结构补救：上一行刚结束、首列像参数名、整行 ≥2 列 时也视为新行
_NAME_LIKE_RE = re.compile(r"^[@A-Za-z_][A-Za-z0-9_@./\-]*$")


def extract_param_names(body_lines: list[str]) -> list[str]:
    """从一个表的正文里抽取"参数名称"（每个新行的第一列）。

    不做去重：同名重复通常代表嵌套字段（如 Members 下的 @odata.id），丢弃会丢信息。

    两条新行判定规则：
      ① 类型命中（白名单/后缀）——is_new_row
      ② 结构补救——上一行没有续行过 & 首列是标识符 & ≥2 列
         覆盖类型列漏填的行，如 "NameServers  指定网口地址为动态模式时，所需的DNS服务器信息。"
    """
    names: list[str] = []
    iter_lines = iter(body_lines)
    # 跳过表头（第一个非空行）
    for line in iter_lines:
        if line.strip():
            break

    in_row = False          # 是否有"当前行"
    cont_count = 0          # 当前行已吃到的续行数量
    for line in iter_lines:
        if not line.strip():
            continue
        cols = split_columns(line)
        if not cols:
            continue

        type_hit = is_new_row(cols)
        struct_hit = (
            not type_hit
            and in_row
            and cont_count == 0
            and len(cols) >= 2
            and bool(_NAME_LIKE_RE.match(cols[0]))
        )

        if type_hit or struct_hit:
            # 过滤首列不是参数名长相的行——如 "文件传输协议包括：sftp" 这种中文描述
            # 被 col[1]='-' 触发 type_hit=True，但首列不像参数名，忽略它
            if _NAME_LIKE_RE.match(cols[0]):
                names.append(cols[0])
            in_row = True
            cont_count = 0
        else:
            if in_row:
                cont_count += 1
    return names


def classify_table(title: str) -> str:
    lower = title.lower()
    if "path" in lower:
        return "path"
    if "header" in lower:
        return "header"
    if "body" in lower:
        return "body"
    if "query" in lower:
        return "query"
    if "response" in lower or "响应" in title or "返回" in title:
        return "response"
    return "other"


# 表格标题：可选 "表X-XXX " 前缀 + 可选 Path/Header/Body/Query/Response + "参数列表"
# 覆盖实际见到的三种写法：
#   "表4-114 Path参数列表" / "表4-117 Response参数列表" / "Response参数列表"
_TABLE_TITLE_RE = re.compile(
    r"^(?:表\s*[\d\-.]+\s+)?(?:Path|Header|Body|Query|Response)?参数列表\s*$"
)


def _is_table_title(s: str) -> bool:
    return bool(_TABLE_TITLE_RE.match(s))


def iter_tables(lines: list[str]):
    """拆表。标题支持 "表X-XXX …参数列表" 与纯 "…参数列表" 两种写法。"""
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if not _is_table_title(s):
            i += 1
            continue
        title = s
        j = i + 1
        body: list[str] = []
        while j < n:
            tt = lines[j].strip()
            if _is_table_title(tt):
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


# =================== 组装接口 ===================

def first_non_empty(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return ""


def build_interface(section: dict) -> Interface:
    subs = split_subsections(section["lines"])
    params = Params()

    for title, body_lines in iter_tables(subs["请求参数"]):
        names = extract_param_names(body_lines)
        category = classify_table(title)
        if category in ("path", "header", "body", "query"):
            getattr(params, category).extend(names)

    for _, body_lines in iter_tables(subs["响应参数"]):
        params.response.extend(extract_param_names(body_lines))

    return Interface(
        section=section["number"],
        title=section["title"],
        method=first_non_empty(subs["调用方法"]),
        uri=first_non_empty(subs["URI"]),
        params=params,
    )


# =================== 输出 ===================

def dump_yaml(data: dict, out: Path) -> Path:
    try:
        import yaml
    except ImportError:
        print("提示：未安装 PyYAML，自动改输出 JSON。`pip install pyyaml` 可切回 YAML。",
              file=sys.stderr)
        out = out.with_suffix(".json")
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def str_representer(dumper, value):
        if "\n" in value:
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", value)

    yaml.add_representer(str, str_representer, Dumper=yaml.SafeDumper)
    out.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    return out


# =================== 入口 ===================

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        inp = Path(argv[1])
        out = (
            Path(argv[2])
            if len(argv) > 2
            else inp.with_suffix(".interfaces.yaml")
        )
    else:
        inp = DEFAULT_INPUT
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = DEFAULT_OUTPUT_DIR / f"{inp.stem}.interfaces.yaml"
    return inp, out


def _write_uris(interfaces: list[Interface], out: Path) -> None:
    lines: list[str] = []
    for iface in interfaces:
        if iface.method:
            lines.append(f"[{iface.method}] {iface.uri}")
        else:
            lines.append(iface.uri)
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main() -> None:
    inp, out = _resolve_io(sys.argv)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    text = read_source(inp)
    all_sections = split_sections(text)
    sections = dedup_sections(all_sections)
    dropped = len(all_sections) - len(sections)

    interfaces: list[Interface] = []
    for section in sections:
        if not _section_has_uri(section):
            continue
        try:
            iface = build_interface(section)
        except Exception as exc:  # pragma: no cover
            print(f"WARN: 解析 {section['number']} {section['title']} 失败: {exc}",
                  file=sys.stderr)
            continue
        if iface.uri:
            interfaces.append(iface)

    data = {"interfaces": [asdict(i) for i in interfaces]}
    final_yaml = dump_yaml(data, out)

    # 顺带写 <stem>.uris.txt：每行 "[METHOD] URI"，顺序与 yaml 里的 interfaces 一致
    # out.stem 对 "xxx.interfaces.yaml" 得到 "xxx.interfaces"；再 Path(...).stem 得到 "xxx"
    base_stem = Path(out.stem).stem if "." in out.stem else out.stem
    uris_path = out.parent / f"{base_stem}.uris.txt"
    _write_uris(interfaces, uris_path)

    dup_note = f"，去重 {dropped} 条章节" if dropped else ""
    print(f"已提取 {len(interfaces)} 个接口{dup_note}")
    print(f"  YAML: {final_yaml}")
    print(f"  URIs: {uris_path}")


if __name__ == "__main__":
    main()
