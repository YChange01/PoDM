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
- params.body       : 请求 body JSON 中**所有深度**的 key（保序去重）
- params.response   : 响应示例 JSON 中**所有深度**的 key（保序去重）
  json.loads 失败（文档常见漏逗号等）时回退到 "key": 正则，结果等价。

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
    SECTION_MARKERS,
    Interface,
    Params,
    _section_has_uri,
    dedup_sections,
    split_sections,
)


# ---- 本脚本私有的 split_subsections ------------------------------------
# 与 extract_interfaces.py 的版本的唯一区别：marker 与尾部数字之间允许空格。
# 示例里的 "请求示例 1" / "响应示例 2" 带空格是常见写法，但表格版不需要
# 这种兼容（原写死 "响应参数1"/"响应参数2" 居多），所以两边各自维护一份，
# 互不影响。
_EX_MARKER_RE = re.compile(
    r"^(" + "|".join(re.escape(m) for m in SECTION_MARKERS) + r")\s*\d*$"
)


def _split_subsections(lines: list[str]) -> dict[str, list[str]]:
    subs: dict[str, list[str]] = {m: [] for m in SECTION_MARKERS}
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        m = _EX_MARKER_RE.match(stripped)
        if m:
            current = m.group(1)  # 归到基础 marker (去掉数字后缀)
            continue
        if current is not None:
            subs[current].append(line)
    return subs

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"

_HTTP_FIRST_RE = re.compile(r"(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s+HTTP/\S+")
# header: "Name: value"，名字允许大小写字母、数字、短横线、下划线
_HEADER_RE = re.compile(r"([A-Za-z][\w-]*)\s*:\s*\S+")
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


def _find_all_bodies(text: str) -> list[str]:
    """顺序找出 text 里所有顶层平衡的 {...} 或 [...]。

    找到一个就跳到它结束位置再找下一个，不会把嵌套的 {} 当独立 body。
    """
    bodies: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        positions = [p for p in (text.find("{", i), text.find("[", i)) if p != -1]
        if not positions:
            break
        start = min(positions)
        open_ch = text[start]
        close_ch = "}" if open_ch == "{" else "]"
        depth = 0
        end = -1
        for j in range(start, n):
            if text[j] == open_ch:
                depth += 1
            elif text[j] == close_ch:
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        if end > 0:
            bodies.append(text[start:end])
            i = end
        else:
            i = start + 1
    return bodies


_JSON_KEY_RE = re.compile(r'"([@A-Za-z_][\w@.\-]*)"\s*:')


def _walk_keys(obj) -> list[str]:
    """递归收集 dict 里所有 key（含嵌套 list/dict），保留首次出现顺序。"""
    out: list[str] = []

    def walk(node) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                out.append(k)
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)
    return out


def _json_all_keys(body_raw: str) -> list[str]:
    """抓 body 里所有 "key": 的 key（任意深度），保序去重。

    先尝试 json.loads + 递归 walk；失败（文档里常见漏逗号之类小毛病）
    退化到正则，把所有 "…": 形式的 key 抓下来。
    """
    try:
        raw = _walk_keys(json.loads(body_raw))
    except Exception:
        raw = [m.group(1) for m in _JSON_KEY_RE.finditer(body_raw)]
    return _dedup_keep_order(raw)


def parse_request_example(lines: list[str]) -> dict | None:
    """解析"请求示例"子块。**多份**请求示例 (请求示例 1/2/3/…) 会合并解析：
    method/uri 取第一个，header/body/path/query 取所有变体的并集（去重保序）。
    """
    raw = "\n".join(lines).strip()
    if not raw:
        return None
    matches = list(_HTTP_FIRST_RE.finditer(raw))
    if not matches:
        return None

    first = matches[0]
    method, uri = first.group(1), first.group(2)

    all_headers: list[str] = []
    all_body_keys: list[str] = []
    for idx, m in enumerate(matches):
        end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw)
        block = raw[m.end() : end_pos]
        body_raw = _find_body(block)
        headers_section = block if body_raw is None else block.split(body_raw, 1)[0]
        all_headers.extend(hm.group(1) for hm in _HEADER_RE.finditer(headers_section))
        if body_raw:
            all_body_keys.extend(_json_all_keys(body_raw))

    headers = _dedup_keep_order(all_headers)
    body_keys = _dedup_keep_order(all_body_keys)

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
    """解析"响应示例"子块。**多份**响应示例的 JSON 顶层均被抓，结果取并集去重。"""
    raw = "\n".join(lines).strip()
    if not raw:
        return []
    all_keys: list[str] = []
    for body in _find_all_bodies(raw):
        all_keys.extend(_json_all_keys(body))
    return _dedup_keep_order(all_keys)


def build_interface(section: dict) -> Interface | None:
    subs = _split_subsections(section["lines"])
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
