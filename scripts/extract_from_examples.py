"""基于"请求示例 / 响应示例"的 HTTP 代码块提取 URI 与参数。

与基于参数表的 extract_from_tables.py **平行**，区别只在数据源：
- extract_from_tables.py 读"请求参数/响应参数"里的表格
- extract_from_examples.py 读"请求示例/响应示例"里的 HTTP 报文和 JSON

对同一份 docx 分别跑两个脚本，再 diff 两份 yaml，就能发现"表格写了但示例没发"
/ "示例发了但表格没列" 的文档不自洽。

提取规则：
- method / uri      : 从 HTTP 首行 "METHOD /path HTTP/1.1"
- params.path       : URI 里的 {xxx} 占位符（顺序保留）
- params.query      : URI 里 ?a=x&b=y 的键名
- params.header     : 首行后、body 之前所有 "Name: value" 里的 Name
- params.body       : 请求 body JSON 中**所有深度**的 key（保序去重）
- params.response   : 响应示例 JSON 中**所有深度**的 key（保序去重）
  json.loads 失败（文档常见漏逗号等）时回退到 "key": 正则。

输出（output/）：
  <stem>.example.interfaces.yaml      字段同 interfaces.yaml
  <stem>.example.uris.txt             每行 "[METHOD] URI"
  <stem>.example.warnings.txt         整条丢弃的 section（如 4.10.4.2 缺 HTTP 首行；仅有时才创建）

用法:
    python3 scripts/extract_from_examples.py                       # 默认输入
    python3 scripts/extract_from_examples.py <path.docx>

依赖：仅 Python 3 标准库；装了 PyYAML 走 yaml，否则自动回退 JSON。

模块组织：
    - 文档结构识别（章节/marker/iter_tables）→ _doc_structure
    - 数据类与文件输出（Params/Interface/dump_yaml）→ _yaml_io
    - 本文件保留：HTTP 首行/header 正则、JSON 平衡括号、key 递归
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from _doc_structure import (  # noqa: E402
    dedup_sections,
    section_has_uri,
    split_sections,
    split_subsections,
)
from _yaml_io import (  # noqa: E402
    Interface,
    Params,
    dedup_keep_order,
    dump_yaml,
    write_uris,
    write_warnings,
)

# 向后兼容别名：why_missing 还按 _split_subsections 名字 import；统一后两边同源。
_split_subsections = split_subsections


# =================== HTTP 报文解析 ===================

# 宽容匹配 HTTP 首行，兼容文档里常见的排版手滑：
#   - METHOD 和 URI 之间缺空格： "POST/redfish/v1/..."           → \s* 允许 0 空格
#   - URI 段中夹空格：           "... /Storage. ImportFC ..."   → URI 用 lazy .*?
#   - URI 和 HTTP/x.y 粘连：      "...PoDImportConfigurationHTTP/1.1" → 后一个 \s* 也是 0 空格
# 这样 examples 路径里能把文档作者这些小手滑抓进来，原样带 bug 输出——
# diff_uris.py 据此指出差异，作者按清单改 doc。
_HTTP_FIRST_RE = re.compile(r"(GET|POST|PUT|PATCH|DELETE)\s*(\S.*?)\s*HTTP/\S+")
# header: "Name: value"，名字允许大小写字母、数字、短横线、下划线
_HEADER_RE = re.compile(r"([A-Za-z][\w-]*)\s*:\s*\S+")
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")
_JSON_KEY_RE = re.compile(r'"([@A-Za-z_][\w@.\-]*)"\s*:')


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

    先尝试 json.loads + 递归 walk；失败（文档里常见漏逗号 / 多余 `]` / `&nbsp;`
    HTML 实体）退化到正则，把所有 "…": 形式的 key 抓下来。
    """
    try:
        raw = _walk_keys(json.loads(body_raw))
    except Exception:
        raw = [m.group(1) for m in _JSON_KEY_RE.finditer(body_raw)]
    return dedup_keep_order(raw)


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

    headers = dedup_keep_order(all_headers)
    body_keys = dedup_keep_order(all_body_keys)

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
    return dedup_keep_order(all_keys)


# =================== 组装接口 ===================

def build_interface(section: dict) -> tuple[Interface | None, str | None]:
    """返回 (Interface, warning)。warning 非 None 时表示整条被跳过的原因。

    跳过原因示例：
      - "请求示例 段无 HTTP 首行 / 段为空"——4.10.4.2 是真实 case，作者没写
        "POST /redfish/v1/SessionService/Sessions HTTP/1.1"
    """
    subs = split_subsections(section["lines"])
    req = parse_request_example(subs.get("请求示例", []))
    if req is None:
        return None, "请求示例 段无 HTTP 首行 / 段为空，整条丢弃"
    resp_keys = parse_response_example(subs.get("响应示例", []))
    return (
        Interface(
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
        ),
        None,
    )


# =================== 入口 ===================

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def main() -> None:
    args = sys.argv[1:]
    path = Path(args[0]) if args else DEFAULT_INPUT
    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    text = read_source(path)
    sections = dedup_sections(split_sections(text))

    warnings: list[str] = []
    interfaces: list[Interface] = []
    for sec in sections:
        if not section_has_uri(sec):
            continue
        iface, warn = build_interface(sec)
        if warn:
            warnings.append(f"{sec['number']}\t{sec['title']}\t{warn}")
            continue
        interfaces.append(iface)

    stem = path.stem
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    yaml_path = DEFAULT_OUTPUT_DIR / f"{stem}.example.interfaces.yaml"
    uris_path = DEFAULT_OUTPUT_DIR / f"{stem}.example.uris.txt"
    warn_path = DEFAULT_OUTPUT_DIR / f"{stem}.example.warnings.txt"

    final_yaml = dump_yaml({"interfaces": [asdict(i) for i in interfaces]}, yaml_path)
    write_uris(interfaces, uris_path)
    written_warn = write_warnings(warnings, warn_path)

    print(f"已提取 {len(interfaces)} 个示例接口")
    print(f"  YAML:  {final_yaml}")
    print(f"  URIs:  {uris_path}")
    if written_warn:
        print(f"  WARN:  {written_warn} ({len(warnings)} 条)")


if __name__ == "__main__":
    main()
