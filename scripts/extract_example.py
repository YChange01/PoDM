"""基于"请求示例 / 响应示例"的 HTTP 代码块提取 URI 与参数。

与基于参数表的 extract_interfaces.py **平行**，区别只在数据源：
- extract_interfaces.py 读"请求参数/响应参数"里的表格
- extract_example.py   读"请求示例/响应示例"里的 HTTP 报文和 JSON

对同一份 docx 分别跑两个脚本，再 diff 两份 yaml，就能发现
"表格写了但示例没发" / "示例发了但表格没列" 的文档不自洽。

提取规则：
- method / uri      : 从 HTTP 首行 "METHOD /path HTTP/1.1"
- params.path       : URI 里的 {xxx} 占位符（顺序保留）
- params.query      : URI 里 ?a=x&b=y 的键名
- params.header     : 首行后、body 之前所有 "Name: value" 里的 Name
- params.body       : 请求 body JSON 的顶层键（json.loads 失败时回退正则）
- params.response   : 响应示例 JSON 的顶层键

两份输出都写到 output/：
  output/<stem>.example.uris.txt          每行 "[METHOD] URI"
  output/<stem>.example.interfaces.yaml   字段同 interfaces.yaml

用法:
    python3 scripts/extract_example.py                       # 默认输入
    python3 scripts/extract_example.py <path.docx>

依赖：仅 Python 3 标准库；装了 PyYAML 走 yaml，否则自动回退 JSON。
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from extract_interfaces import (  # noqa: E402
    Interface,
    Params,
    _section_has_uri,
    dedup_sections,
    split_sections,
    split_subsections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"

_HTTP_FIRST_RE = re.compile(r"(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s+HTTP/\S+")
# header: "Name: value"，名字允许大小写字母、数字、短横线、下划线
_HEADER_RE = re.compile(r"([A-Za-z][\w-]*)\s*:\s*\S+")
# JSON key 允许 @odata.context / Members@odata.count / Id 等
_JSON_KEY_RE = re.compile(r'"([@\w.\-]+)"\s*:')
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


def _dedup_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def _extract_balanced(text: str, open_ch: str) -> str | None:
    """在 text 里找第一个 open_ch，返回其到匹配 close 之间的平衡子串。"""
    close_ch = "}" if open_ch == "{" else "]"
    start = text.find(open_ch)
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def _find_body(text: str) -> str | None:
    """优先 '{...}'，没有再试 '[...]'。"""
    candidates = []
    for ch in ("{", "["):
        body = _extract_balanced(text, ch)
        if body:
            candidates.append((text.find(ch), body))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]


def _json_top_keys(body_raw: str) -> list[str]:
    """优先 json.loads；失败（示例里值常为占位符不合法）时退化为 "key": 正则。"""
    try:
        obj = json.loads(body_raw)
        if isinstance(obj, dict):
            return list(obj.keys())
    except Exception:
        pass
    return _dedup_keep_order(m.group(1) for m in _JSON_KEY_RE.finditer(body_raw))


def parse_request_example(lines: list[str]) -> dict | None:
    raw = "\n".join(lines).strip()
    if not raw:
        return None
    m = _HTTP_FIRST_RE.search(raw)
    if not m:
        return None
    method, uri = m.group(1), m.group(2)
    after = raw[m.end() :]

    body_raw = _find_body(after)
    headers_section = after if body_raw is None else after.split(body_raw, 1)[0]

    headers = _dedup_keep_order(hm.group(1) for hm in _HEADER_RE.finditer(headers_section))
    body_keys = _json_top_keys(body_raw) if body_raw else []

    path_keys = _PLACEHOLDER_RE.findall(uri)
    query_keys: list[str] = []
    if "?" in uri:
        _, qs = uri.split("?", 1)
        for pair in qs.split("&"):
            if "=" in pair:
                query_keys.append(pair.split("=", 1)[0])

    return {
        "method": method,
        "uri": uri,
        "path": path_keys,
        "query": query_keys,
        "header": headers,
        "body": body_keys,
    }


def parse_response_example(lines: list[str]) -> list[str]:
    raw = "\n".join(lines).strip()
    body = _find_body(raw)
    return _json_top_keys(body) if body else []


def build_interface(section: dict) -> Interface | None:
    subs = split_subsections(section["lines"])
    req = parse_request_example(subs.get("请求示例", []))
    if req is None:
        return None
    resp_keys = parse_response_example(subs.get("响应示例", []))
    return Interface(
        section=section["number"],
        title=section["title"],
        method=req["method"],
        uri=req["uri"],
        params=Params(
            path=req["path"],
            header=req["header"],
            body=req["body"],
            query=req["query"],
            response=resp_keys,
        ),
    )


def dump_yaml(data: dict, out: Path) -> Path:
    try:
        import yaml
    except ImportError:
        print("提示：未安装 PyYAML，自动改输出 JSON。`pip install pyyaml` 可切回 YAML。",
              file=sys.stderr)
        out = out.with_suffix(".json")
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def repr_str(dumper, value):
        if "\n" in value:
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", value)

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
    out.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    return out


def main() -> None:
    args = sys.argv[1:]
    path = Path(args[0]) if args else DEFAULT_INPUT
    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    text = read_source(path)
    sections = dedup_sections(split_sections(text))

    interfaces: list[Interface] = []
    for sec in sections:
        if not _section_has_uri(sec):
            continue
        iface = build_interface(sec)
        if iface is not None:
            interfaces.append(iface)

    stem = path.stem
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = DEFAULT_OUTPUT_DIR / f"{stem}.example.interfaces.yaml"
    uris_path = DEFAULT_OUTPUT_DIR / f"{stem}.example.uris.txt"

    final_yaml = dump_yaml({"interfaces": [asdict(i) for i in interfaces]}, yaml_path)

    uri_lines: list[str] = []
    for iface in interfaces:
        if iface.method:
            uri_lines.append(f"[{iface.method}] {iface.uri}")
        else:
            uri_lines.append(iface.uri)
    uris_path.write_text(
        "\n".join(uri_lines) + ("\n" if uri_lines else ""),
        encoding="utf-8",
    )

    print(f"已提取 {len(interfaces)} 个示例接口")
    print(f"  YAML:  {final_yaml}")
    print(f"  URIs:  {uris_path}")


if __name__ == "__main__":
    main()
