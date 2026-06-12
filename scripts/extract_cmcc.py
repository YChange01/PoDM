#!/usr/bin/env python3
"""Extract CMCC Redfish interfaces plus request/response parameter names.

The China Mobile requirement document uses a BMC-like layout:

- sections such as ``6.1.2.1 查询服务器资产``;
- subsections such as ``命令格式`` / ``参数说明`` / ``输出说明``;
- method and URL inside ``命令格式``;
- request parameters mixed in one ``参数说明`` table;
- response fields usually in ``输出说明`` tables, and occasionally in a later
  ``参数说明`` table headed by ``字段 / 类型 / 说明``.

Output schema follows ``extract_bmc.py``:
``interfaces[].params.path/header/body/query/response`` are lists of names.
"""
from __future__ import annotations

import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cmcc_docx_utils import read_source  # noqa: E402
from _doc_structure import HEADING_RE, _strip_trailing_pageno, split_columns  # noqa: E402
from _yaml_io import Interface, Params, dedup_keep_order, dump_yaml, write_uris  # noqa: E402


DEFAULT_INPUT = Path("data/20260610/附件5：中国移动服务器Redfish管理接口要求V6.1.0-v20260604.docx")
DEFAULT_OUTPUT = Path("output/20260610/cmcc.interfaces.yaml")

CMCC_MARKERS = (
    "命令功能",
    "命令格式",
    "参数说明",
    "使用指南",
    "使用实例",
    "输出说明",
)
MARKER_RE = re.compile(
    r"^(" + "|".join(re.escape(marker) for marker in CMCC_MARKERS) + r")\s*[:：]?\s*$"
)
METHOD_RE = re.compile(r"^(?:操作类型|请求方法)\s*[:：]\s*(\w+)\s*$", re.IGNORECASE)
URL_RE = re.compile(
    r"^(?:[一-鿿]{1,8}\s*[:：]\s*)?"
    r"[一-鿿]{0,3}URL\s*[:：]\s*"
    r"(.*)$",
    re.IGNORECASE,
)
INLINE_REQUEST_HEADER_RE = re.compile(r"^请求头\s*[:：]\s*(.+)$")
HEADER_LINE_RE = re.compile(r"^([A-Za-z][\w-]*)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*$")
JSON_KEY_RE = re.compile(r'["“]([@A-Za-z_][\w@.\-]*)["”]\s*[:：]')
JSON_VALUE_PLACEHOLDER_RE = re.compile(
    r"[:：]\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:[,，}\]\n]|$)"
)
TABLE_TITLE_RE = re.compile(r"^表\s*\d+(?:[-.]\d+)?\s+\S")
TYPE_VALUES = {
    "string",
    "str",
    "integer",
    "int",
    "number",
    "float",
    "double",
    "boolean",
    "bool",
    "array",
    "object",
    "enum",
    "null",
    "uri",
    "url",
    "字符串",
    "字符",
    "数字",
    "整数",
    "整型",
    "布尔",
    "布尔值",
    "对象",
    "数组",
    "列表",
    "枚举",
    "自定义属性",
}
TYPE_SUFFIX_RE = re.compile(r"^.{0,24}(列表|数组|对象|集合|属性|字典|映射|型)$")
FIELD_NAME_RE = re.compile(r"^[@A-Za-z_][A-Za-z0-9_@.\-]*$")
PATH_KEYWORDS = {"redfish", "v1", "actions", "oem", "public", "cmcc"}
IGNORED_REQUEST_NAMES = {"device_ip"}
NON_BODY_VALUE_WORDS = {"true", "false", "null", "none"}


def normalize_source_text(text: str) -> str:
    """Put pasted/flattened headings on their own lines where possible."""
    lines: list[str] = []
    heading_boundary = re.compile(r"(?<!^)(?<![\d.])(?=\d+(?:\.\d+){2,}\s+[^\s/{])")
    for line in text.replace("\u3000", " ").replace("\xa0", " ").splitlines():
        parts = [part.strip() for part in heading_boundary.split(line) if part.strip()]
        lines.extend(parts or [line])
    return "\n".join(lines)


def split_sections(text: str) -> list[dict[str, object]]:
    sections: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in normalize_source_text(text).splitlines():
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


def split_command_blocks(text: str) -> list[dict[str, object]]:
    """Split each command format block as one interface.

    Some Word files store ``6.1.x`` numbering in OOXML numbering metadata rather
    than literal paragraph text. The lightweight reader then sees only title
    text, so heading-based splitting may either yield no sections or only coarse
    parent sections. Use each ``命令格式`` block as an interface boundary and infer
    the title from the line before ``命令功能``.
    """
    lines = normalize_source_text(text).splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if re.match(r"^命令格式\s*[:：]?\s*$", line.strip())
    ]
    if not starts:
        starts = [
            index
            for index, line in enumerate(lines)
            if METHOD_RE.match(line.strip()) or URL_RE.match(line.strip())
        ]

    sections: list[dict[str, object]] = []
    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        number, title = infer_heading_before_command(lines, start)
        sections.append(
            {
                "number": number,
                "title": title,
                "lines": lines[start:end],
            }
        )
    return sections


def infer_heading_before_command(lines: list[str], command_start: int) -> tuple[str, str]:
    title_limit = 80
    for index in range(command_start - 1, -1, -1):
        stripped = lines[index].strip()
        if re.match(r"^命令功能\s*[:：]?\s*$", stripped):
            return parse_heading_title(previous_title_line(lines, index, title_limit))
    return parse_heading_title(previous_title_line(lines, command_start, title_limit))


def parse_heading_title(line: str) -> tuple[str, str]:
    stripped = line.strip(" \t▪■●◆◇-")
    match = HEADING_RE.match(stripped)
    if not match:
        return "", stripped
    return match.group(1), _strip_trailing_pageno(match.group(2).strip())


def previous_title_line(lines: list[str], before_index: int, title_limit: int) -> str:
    for index in range(before_index - 1, -1, -1):
        stripped = lines[index].strip()
        if not stripped:
            continue
        if MARKER_RE.match(stripped) or TABLE_TITLE_RE.match(stripped):
            continue
        if "\t" in stripped:
            continue
        if len(stripped) <= title_limit:
            return stripped
    return ""


def split_subsections(lines: list[str]) -> dict[str, list[str]]:
    subsections: dict[str, list[str]] = {marker: [] for marker in CMCC_MARKERS}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        match = MARKER_RE.match(stripped)
        if match:
            current = match.group(1)
            continue
        if current is not None:
            subsections[current].append(line)
    return subsections


def extract_command_region(lines: list[str]) -> list[str]:
    start = 0
    for index, line in enumerate(lines):
        if re.search(r"命令格式\s*[:：]?\s*$", line.strip()):
            start = index + 1
            break
        if METHOD_RE.match(line.strip()) or URL_RE.match(line.strip()):
            start = index
            break

    out: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if MARKER_RE.match(stripped) and not re.match(r"^命令格式", stripped):
            break
        if re.match(r"^(参数说明|使用指南|使用实例|输出说明)\s*[:：]?\s*$", stripped):
            break
        out.append(line)
    return out


def first_non_empty(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return ""


def parse_command_format(lines: list[str]) -> dict[str, list[str] | str]:
    method = ""
    uri = ""
    header_names: list[str] = []
    header_values: list[str] = []
    body_placeholders: list[str] = []
    in_headers = False
    in_body = False
    body_lines: list[str] = []

    for index, line in enumerate(lines):
        stripped = line.strip()
        method_match = METHOD_RE.match(stripped)
        if method_match:
            method = method_match.group(1).upper()

        url_match = URL_RE.match(stripped)
        if url_match:
            inline = url_match.group(1).strip()
            uri = inline or first_non_empty(lines[index + 1 :])

        inline_header = INLINE_REQUEST_HEADER_RE.match(stripped)
        if inline_header:
            in_headers = True
            in_body = False
            parse_header_line(inline_header.group(1), header_names, header_values)
            continue

        if re.match(r"^请求头\s*[:：]?\s*$", stripped):
            in_headers = True
            in_body = False
            continue
        if re.match(r"^请求消息体\s*[:：]\s*无\s*$", stripped):
            in_headers = False
            in_body = False
            continue
        if re.match(r"^请求消息体\s*[:：]?\s*$", stripped):
            in_headers = False
            in_body = True
            continue

        if in_headers:
            parse_header_line(stripped, header_names, header_values)
        elif in_body:
            body_lines.append(line)

    body_text = "\n".join(body_lines)
    body_placeholders.extend(extract_body_placeholders(body_text))

    return {
        "method": method,
        "uri": uri,
        "header_names": dedup_keep_order(header_names),
        "header_values": dedup_keep_order(header_values),
        "body_placeholders": dedup_keep_order(body_placeholders),
        "path_keys": extract_path_keys(uri),
        "query_keys": extract_query_keys(uri),
    }


def parse_header_line(line: str, names: list[str], values: list[str]) -> None:
    match = HEADER_LINE_RE.match(line.strip())
    if not match:
        return
    names.append(match.group(1))
    values.append(normalize_param_name(match.group(2)))


def extract_body_placeholders(body_text: str) -> list[str]:
    if not body_text.strip():
        return []
    placeholders: list[str] = []
    keys = set(JSON_KEY_RE.findall(body_text))
    for match in JSON_VALUE_PLACEHOLDER_RE.finditer(body_text):
        value = normalize_param_name(match.group(1))
        if value.lower() in NON_BODY_VALUE_WORDS:
            continue
        if value in keys:
            continue
        placeholders.append(value)
    return dedup_keep_order(placeholders)


def normalize_param_name(value: str) -> str:
    return re.sub(r"\s+", "", value.strip())


def extract_path_keys(uri: str) -> list[str]:
    if not uri:
        return []
    path = re.sub(r"^https?://[^/]+", "", uri).split("?", 1)[0]
    keys: list[str] = []
    for segment in path.strip("/").split("/"):
        normalized = normalize_param_name(segment)
        if not normalized or normalized.lower() in PATH_KEYWORDS:
            continue
        if re.fullmatch(r"[a-z][a-z0-9_]*", normalized):
            keys.append(normalized)
    return dedup_keep_order(keys)


def extract_query_keys(uri: str) -> list[str]:
    if "?" not in uri:
        return []
    query = uri.split("?", 1)[1]
    keys: list[str] = []
    for pair in query.split("&"):
        key, sep, _value = pair.partition("=")
        if sep and key:
            keys.append(key.strip())
    return dedup_keep_order(keys)


def looks_like_type(value: str) -> bool:
    if not value.strip():
        return False
    head = re.split(r"[,，、;；:：\s]", value.strip(), maxsplit=1)[0]
    return head.lower() in TYPE_VALUES or head in TYPE_VALUES or bool(TYPE_SUFFIX_RE.match(head))


def parse_request_params(
    lines: list[str],
    path_keys: list[str],
    header_values: list[str],
    body_placeholders: list[str],
    query_keys: list[str],
) -> Params:
    params = Params()
    key_to_category: dict[str, str] = {}
    for name in path_keys:
        key_to_category[name.lower()] = "path"
    for name in header_values:
        key_to_category[name.lower()] = "header"
    for name in body_placeholders:
        key_to_category[name.lower()] = "body"
    for name in query_keys:
        key_to_category[name.lower()] = "query"

    in_request_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped or TABLE_TITLE_RE.match(stripped):
            continue
        cols = split_columns(line)
        if not cols:
            continue
        first = normalize_param_name(cols[0])
        if first == "参数":
            in_request_table = True
            continue
        if first == "字段":
            in_request_table = False
            continue
        if not in_request_table or not looks_like_param_name(first):
            continue
        if first.lower() in IGNORED_REQUEST_NAMES:
            continue

        category = key_to_category.get(first.lower())
        if category is None:
            category = "body" if body_placeholders else ""
        add_param(params, category, first)

    for category, names in (
        ("path", path_keys),
        ("header", header_values),
        ("query", query_keys),
    ):
        for name in names:
            add_param(params, category, name)
    return params


def looks_like_param_name(value: str) -> bool:
    return bool(re.fullmatch(r"[$@A-Za-z_][A-Za-z0-9_$@./\-]*", value))


def add_param(params: Params, category: str, name: str) -> None:
    if category not in {"path", "header", "body", "query", "response"}:
        return
    bucket = getattr(params, category)
    if name not in bucket:
        bucket.append(name)


def parse_response_fields(lines: list[str]) -> list[str]:
    fields: list[str] = []
    in_response_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped or TABLE_TITLE_RE.match(stripped):
            continue
        cols = split_columns(line)
        if not cols:
            continue
        first = normalize_param_name(cols[0])
        if first == "字段":
            in_response_table = True
            continue
        if first == "参数":
            in_response_table = False
            continue
        if (
            in_response_table
            and len(cols) >= 2
            and FIELD_NAME_RE.match(first)
            and looks_like_type(cols[1])
            and first not in fields
        ):
            fields.append(first)
    return fields


def build_interface(section: dict[str, object]) -> Interface | None:
    lines = list(section["lines"])
    subsections = split_subsections(lines)
    command_lines = subsections["命令格式"] or extract_command_region(lines)
    command = parse_command_format(command_lines)
    uri = str(command["uri"])
    if not uri:
        return None

    params = parse_request_params(
        subsections["参数说明"],
        list(command["path_keys"]),
        list(command["header_values"]),
        list(command["body_placeholders"]),
        list(command["query_keys"]),
    )
    params.response = parse_response_fields(subsections["输出说明"] + subsections["参数说明"])
    return Interface(
        section=str(section["number"]),
        title=str(section["title"]),
        method=str(command["method"]),
        uri=uri,
        params=params,
    )


def extract(text: str) -> list[Interface]:
    heading_interfaces = extract_from_sections(split_sections(text))
    command_interfaces = extract_from_sections(split_command_blocks(text))
    if len(command_interfaces) > len(heading_interfaces):
        return command_interfaces
    return heading_interfaces or command_interfaces


def extract_from_sections(sections: list[dict[str, object]]) -> list[Interface]:
    interfaces: list[Interface] = []
    for section in sections:
        iface = build_interface(section)
        if iface is not None:
            interfaces.append(iface)
    return interfaces


def resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if argv:
        input_path = Path(argv[0])
        output_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
        return input_path, output_path
    return DEFAULT_INPUT, DEFAULT_OUTPUT


def main(argv: list[str] | None = None) -> None:
    input_path, output_path = resolve_io(sys.argv[1:] if argv is None else argv)
    if not input_path.exists():
        raise SystemExit(f"输入文件不存在: {input_path}")

    interfaces = extract(read_source(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_yaml = dump_yaml({"interfaces": [asdict(item) for item in interfaces]}, output_path)
    base_stem = Path(output_path.stem).stem if "." in output_path.stem else output_path.stem
    uris_path = output_path.parent / f"{base_stem}.uris.txt"
    write_uris(interfaces, uris_path)

    print(f"已提取 {len(interfaces)} 个 CMCC 接口")
    print(f"  YAML:  {final_yaml}")
    print(f"  URIs:  {uris_path}")


if __name__ == "__main__":
    main()
