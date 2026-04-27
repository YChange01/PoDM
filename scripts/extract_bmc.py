#!/usr/bin/env python3
"""
从 BMC (iBMC300) Redfish 接口文档提取接口和参数信息。

跟 PoDManager 接口文档的结构差异（决定了为什么单独写一份 extractor）：
- **子段 marker**：命令功能 / 命令格式 / 参数说明 / 使用指南 / 使用实例 / 输出说明
  （PoDManager 是：接口功能 / 调用方法 / URI / 请求参数 / 请求示例 / 响应参数 / 响应示例）
- **method + URL**：合并在"命令格式"子段下，
  "操作类型：POST" + "URL：https://device_ip/redfish/v1/..."
- **URL 占位符**：bare word，没有 `{}`（PoDManager 用 `{manager_id}`）
- **参数说明表**：单张表，列数不定（3 列：参数/说明/取值，或 4 列：参数/类型/说明/取值），
  把 path / header / body 占位符全混在一起
- **响应字段**：从"输出说明"表的"字段"列抽
- **请求 / 响应示例**：在"使用实例"子段下，请求 JSON 是模板形式（值是占位符），
  响应 JSON 是真实样例

输出 yaml 沿用 PoDManager schema (Interface/Params)，方便跨文档 diff：
  output/<stem>.bmc.interfaces.yaml
  output/<stem>.bmc.uris.txt
  output/<stem>.bmc.warnings.txt （仅有时才创建）

限制：仅处理 **chapter 3**（接口本体）。chapter 4 是附录（ActionInfo / Basic Auth /
$expand/$select / 错误码等说明文档），不算接口，跳过。

用法：
    python3 scripts/extract_bmc.py
    python3 scripts/extract_bmc.py <docx_path>

依赖：仅 Python 3 标准库 + PyYAML（已在 _yaml_io 处理）。
"""
from __future__ import annotations

import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from _doc_structure import (  # noqa: E402
    HEADING_RE,
    _strip_trailing_pageno,
    split_columns,
)
from _yaml_io import (  # noqa: E402
    Interface,
    Params,
    dedup_keep_order,
    dump_yaml,
    write_uris,
    write_warnings,
)


# ===================== BMC 子段 marker =====================

BMC_MARKERS: tuple[str, ...] = (
    "命令功能", "命令格式", "参数说明", "使用指南", "使用实例", "输出说明",
)
# 兼容数字后缀（"参数说明 1" 之类），跟 PoDManager 的 marker 正则同款思路
_BMC_MARKER_RE = re.compile(
    r"^(" + "|".join(re.escape(m) for m in BMC_MARKERS) + r")\s*\d*$"
)


def split_sections_chapter3(text: str) -> list[dict]:
    """切章节，仅保留 3.x.y（接口本体），跳过 chapter 4 附录。"""
    sections: list[dict] = []
    current: dict | None = None
    for line in text.splitlines():
        stripped = line.strip()
        m = HEADING_RE.match(stripped)
        if m:
            number = m.group(1)
            title = _strip_trailing_pageno(m.group(2).strip())
            if current is not None:
                sections.append(current)
            current = {"number": number, "title": title, "lines": []}
            continue
        if current is not None:
            current["lines"].append(line)
    if current is not None:
        sections.append(current)
    # 仅 chapter 3
    return [s for s in sections if s["number"].startswith("3.")]


def split_subsections_bmc(lines: list[str]) -> dict[str, list[str]]:
    """按 BMC 子段 marker 切，返回 {marker: [lines, ...]}（缺省 marker 为空 list）。"""
    subs: dict[str, list[str]] = {m: [] for m in BMC_MARKERS}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        m = _BMC_MARKER_RE.match(stripped)
        if m:
            current = m.group(1)
            continue
        if current is not None:
            subs[current].append(line)
    return subs


def is_interface_section(sec: dict) -> bool:
    """判断 section 是否是接口小节——存在 '命令格式' marker 行就算。"""
    return any(line.strip() == "命令格式" for line in sec["lines"])


# ===================== 命令格式 解析 =====================

# "操作类型：POST" / "操作类型: POST"
_METHOD_LINE_RE = re.compile(r"^操作类型\s*[:：]\s*(\w+)\s*$")
# URL 行：兼容三种写法
#   "URL：https://..."        基础
#   "URL:https://..."         半角冒号
#   "URL:"                    URL 跨行（value 在下一非空行）
#   "新URL：https://..."      BMC 文档某些修订段用 "新URL" 前缀（22 个 section 中招）
# 允许 marker 前 0-3 个中文字符前缀（"新"/"新版" 之类）。
_URL_LINE_RE = re.compile(r"^[一-鿿]{0,3}URL\s*[:：]\s*(.*)$")
# 请求头里的 "Name: value"（Name 取 ASCII 字母数字短横线下划线）
_HEADER_LINE_RE = re.compile(r"^([A-Za-z][\w-]*)\s*:\s*\S+")
# JSON 里 "key":
_JSON_KEY_RE = re.compile(r'"([@A-Za-z_][\w@.\-]*)"\s*:')


def parse_command_format(lines: list[str]) -> dict:
    """解析 命令格式 子段，提取 method / url / header_names / body_keys。

    URL 可能 inline 在 "URL:" 行，也可能 URL 行后面跟一行才是 URL（doc 排版差异）。
    """
    method = ""
    url = ""

    # method
    for line in lines:
        m = _METHOD_LINE_RE.match(line.strip())
        if m:
            method = m.group(1).upper()
            break

    # URL：找到 "URL:" 行，看 inline 还是下一非空行
    for i, line in enumerate(lines):
        m = _URL_LINE_RE.match(line.strip())
        if m:
            inline = m.group(1).strip()
            if inline:
                url = inline
            else:
                for j in range(i + 1, len(lines)):
                    nxt = lines[j].strip()
                    if nxt:
                        url = nxt
                        break
            break

    # 切 请求头 / 请求消息体 两段
    headers: list[str] = []
    body_text_lines: list[str] = []
    in_headers = False
    in_body = False
    for line in lines:
        s = line.strip()
        # 段落起始 marker（兼容 ":" / "：" 结尾）
        if re.match(r"^请求头\s*[:：]?\s*$", s):
            in_headers = True; in_body = False; continue
        if re.match(r"^请求消息体\s*[:：]?\s*$", s):
            in_headers = False; in_body = True; continue
        # "请求消息体：无" / "请求消息体: 无" 形式：body 段标记结束（关 in_headers）
        if re.match(r"^请求消息体\s*[:：]\s*无\s*$", s):
            in_headers = False; in_body = False; continue
        # 出现下一个已知 marker 就停（如 "参数说明"）——理论上 split_subsections
        # 已经把 命令格式 切出来了，这里不会出现，但防御一下
        if s in BMC_MARKERS:
            break
        if in_headers:
            m = _HEADER_LINE_RE.match(s)
            if m:
                headers.append(m.group(1))
        if in_body:
            body_text_lines.append(line)

    body_text = "\n".join(body_text_lines).strip()
    body_keys: list[str] = []
    if body_text and body_text != "无":
        body_keys = dedup_keep_order(
            [m.group(1) for m in _JSON_KEY_RE.finditer(body_text)]
        )

    return {
        "method": method,
        "url": url,
        "headers": dedup_keep_order(headers),
        "body": body_keys,
    }


# ===================== 输出说明 解析（响应字段） =====================

# 字段名长相：@/字母/_ 开头，可含字母数字 . - _ @
_FIELD_NAME_RE = re.compile(r"^[@A-Za-z_][\w@.\-]*$")


def extract_response_fields(lines: list[str]) -> list[str]:
    """从 输出说明 子段提取响应字段名（每行首列）。

    跳过表头行 ('字段'/'类型'/'说明')。不去重——同名重复通常代表嵌套字段
    （如 RootCertificate.Subject 和 ClientCertificate.Subject 共用 Subject 时）。
    """
    out: list[str] = []
    for line in lines:
        cols = split_columns(line)
        if not cols:
            continue
        first = cols[0]
        if first in ("字段", "类型", "说明", "参数"):
            continue
        if _FIELD_NAME_RE.match(first):
            out.append(first)
    return out


# ===================== URL 占位符识别 =====================

# bare word 占位符：全小写字母，可含下划线和数字。区别于路径段（如 SnmpService）。
_PLACEHOLDER_TOKEN_RE = re.compile(r"^[a-z][a-z_0-9]*$")
# 这些 path 段不是占位符，而是 Redfish 路径关键字
_PATH_KEYWORDS = {"redfish", "v1", "actions", "oem", "huawei", "public"}


def extract_path_placeholders(url: str) -> list[str]:
    """从 BMC URL 中识别 path 占位符。

    去掉 scheme://host 前缀和 query string 后，path 段里全小写 bare word
    token 视为占位符（区别于 'Managers' 'SnmpService' 这种 PascalCase 路径段）。
    """
    if not url:
        return []
    path = re.sub(r"^https?://[^/]+", "", url)
    path = path.split("?", 1)[0]
    out: list[str] = []
    for seg in path.strip("/").split("/"):
        if (_PLACEHOLDER_TOKEN_RE.match(seg)
                and seg.lower() not in _PATH_KEYWORDS):
            out.append(seg)
    return dedup_keep_order(out)


def extract_query_keys(url: str) -> list[str]:
    """从 URL query string 中抽 key 名。"""
    if "?" not in url:
        return []
    qs = url.split("?", 1)[1]
    return [pair.split("=", 1)[0] for pair in qs.split("&") if "=" in pair]


# ===================== 组装接口 =====================

def build_interface(section: dict) -> tuple[Interface | None, str | None]:
    """返回 (Interface, warning)。warning 非 None 表示跳过原因。"""
    subs = split_subsections_bmc(section["lines"])
    cmd_lines = subs.get("命令格式", [])
    if not cmd_lines:
        return None, "命令格式 子段为空"

    cmd = parse_command_format(cmd_lines)
    if not cmd["url"]:
        return None, "命令格式 子段未找到 URL 行"

    response_fields = extract_response_fields(subs.get("输出说明", []))

    iface = Interface(
        section=section["number"],
        title=section["title"],
        method=cmd["method"],
        uri=cmd["url"],
        params=Params(
            path=extract_path_placeholders(cmd["url"]),
            header=cmd["headers"],
            body=cmd["body"],
            query=extract_query_keys(cmd["url"]),
            response=response_fields,
        ),
    )
    return iface, None


# ===================== 入口 =====================

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "华为服务器 iBMC300 Redfish 接口说明_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def main() -> None:
    args = sys.argv[1:]
    path = Path(args[0]) if args else DEFAULT_INPUT
    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    text = read_source(path)
    sections = split_sections_chapter3(text)

    warnings: list[str] = []
    interfaces: list[Interface] = []
    skipped = 0
    for sec in sections:
        if not is_interface_section(sec):
            skipped += 1
            continue
        iface, warn = build_interface(sec)
        if warn:
            warnings.append(f"{sec['number']}\t{sec['title']}\t{warn}")
            continue
        interfaces.append(iface)

    stem = path.stem
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = DEFAULT_OUTPUT_DIR / f"{stem}.bmc.interfaces.yaml"
    uris_path = DEFAULT_OUTPUT_DIR / f"{stem}.bmc.uris.txt"
    warn_path = DEFAULT_OUTPUT_DIR / f"{stem}.bmc.warnings.txt"

    final_yaml = dump_yaml(
        {"interfaces": [asdict(i) for i in interfaces]}, yaml_path
    )
    write_uris(interfaces, uris_path)
    written_warn = write_warnings(warnings, warn_path)

    print(f"已提取 {len(interfaces)} 个 BMC 接口（chapter 3，跳过 {skipped} 个非接口章节）")
    print(f"  YAML:  {final_yaml}")
    print(f"  URIs:  {uris_path}")
    if written_warn:
        print(f"  WARN:  {written_warn} ({len(warnings)} 条)")


if __name__ == "__main__":
    main()
