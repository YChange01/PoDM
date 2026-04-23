"""分析示例路径相对表格路径**漏抓**的接口，每条给出具体原因。

对比 extract_from_tables.py 和 extract_from_examples.py 两条路径后，
有些 section 在表格侧有 URI、但示例侧拿不到。本脚本直接读 .docx，
对每个这样的 section 取出"请求示例"子块原文，诊断为什么 HTTP 首行
没被正则 (GET|POST|PUT|PATCH|DELETE)\\s+(\\S+)\\s+HTTP/\\S+ 抓到。

诊断标签：
  NO_EXAMPLE_MARKER  根本没有 "请求示例" 子块（整节没写）
  EMPTY_EXAMPLE      有标题但正文空/只有 "略" / "无" / "暂无" / "-"
  NO_HTTP_LINE       有正文但没 METHOD uri HTTP/... 那行（给了 curl / 裸 json）
  MALFORMED_HTTP     看到 HTTP 字样但正则认不出（被 Word 粘连/拆行）
  OTHER              兜底

用法：
    python3 scripts/why_missing.py                       # 默认输入 + 默认输出
    python3 scripts/why_missing.py <input.docx>
    python3 scripts/why_missing.py <input.docx> <out.txt>

结果写到 output/why_missing.txt (UTF-8)，终端只打一行摘要。
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from extract_from_tables import (  # noqa: E402
    _section_has_uri,
    build_interface as tables_build_interface,
    dedup_sections,
    split_sections,
)
from extract_from_examples import (  # noqa: E402
    _HTTP_FIRST_RE,
    _split_subsections as ex_split_subsections,
    parse_request_example,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT = REPO_ROOT / "output" / "why_missing.txt"

_EMPTY_SIGNALS = {"略", "无", "暂无", "-", "—", "…"}
_HTTP_LOOSE_RE = re.compile(r"\bHTTP\s*/\s*\d", re.IGNORECASE)


def _diagnose(example_lines: list[str]) -> tuple[str, str]:
    """返回 (标签, 原文摘要 50~200 字)。"""
    if not example_lines:
        return "NO_EXAMPLE_MARKER", ""
    body = "\n".join(example_lines).strip()
    if not body:
        return "EMPTY_EXAMPLE", ""
    # 去掉 "HTTP的示例" 这种小标题再看
    stripped = re.sub(r"^HTTP的示例\s*", "", body, flags=re.MULTILINE).strip()
    if not stripped or stripped in _EMPTY_SIGNALS:
        return "EMPTY_EXAMPLE", body[:200]
    # 是否整体只是一两个字的占位文字
    if len(stripped) < 4 and stripped in _EMPTY_SIGNALS:
        return "EMPTY_EXAMPLE", body[:200]
    if _HTTP_FIRST_RE.search(body):
        # 规则内应能抓到，但如果我们进入这里就是漏了 → 其他兜底
        return "OTHER", body[:200]
    if _HTTP_LOOSE_RE.search(body):
        return "MALFORMED_HTTP", body[:200]
    return "NO_HTTP_LINE", body[:200]


def main() -> None:
    args = sys.argv[1:]
    inp = Path(args[0]) if args else DEFAULT_INPUT
    out = Path(args[1]) if len(args) >= 2 else DEFAULT_OUTPUT
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    text = read_source(inp)
    sections = dedup_sections(split_sections(text))

    missing: list[tuple[str, str, str, str]] = []
    # 这里对每个 section：
    #   1) tables 路径看能否建出 Interface（作为 "表格有" 的判断）
    #   2) examples 路径看 parse_request_example 是否 None
    tables_have = 0
    examples_have = 0
    for sec in sections:
        if not _section_has_uri(sec):
            continue
        try:
            t_iface = tables_build_interface(sec)
        except Exception:
            continue
        if not t_iface.uri:
            continue
        tables_have += 1

        # 用示例路径私有的 _split_subsections（marker 带空格兼容）
        ex_subs = ex_split_subsections(sec["lines"])
        req_lines = ex_subs.get("请求示例", [])
        parsed = parse_request_example(req_lines)
        if parsed is not None and parsed.get("uri"):
            examples_have += 1
            continue

        tag, snippet = _diagnose(req_lines)
        missing.append(
            (sec["number"], sec["title"], f"[{t_iface.method}] {t_iface.uri}", tag)
        )

    # 汇总
    tag_counter: Counter[str] = Counter(m[3] for m in missing)

    lines: list[str] = []
    lines.append(f"输入: {inp}")
    lines.append(
        f"表格路径覆盖 {tables_have} 条 / 示例路径覆盖 {examples_have} 条 / "
        f"漏抓 {len(missing)} 条"
    )
    lines.append("")
    if tag_counter:
        lines.append("漏抓原因分布：")
        for tag, cnt in tag_counter.most_common():
            lines.append(f"  {tag:<20} {cnt}")
        lines.append("")

    # 按标签分组明细
    by_tag: dict[str, list[tuple[str, str, str, str]]] = {}
    for item in missing:
        by_tag.setdefault(item[3], []).append(item)

    for tag in sorted(by_tag, key=lambda t: -len(by_tag[t])):
        rows = by_tag[tag]
        lines.append(f"## {tag}  ({len(rows)} 条)")
        for sec_num, title, tbl_uri, _ in rows:
            lines.append(f"  {sec_num}  {title}")
            lines.append(f"    tables: {tbl_uri}")
            # 把 req_lines 原文再取一遍放进去（省内存就再扫一次）
            for sec in sections:
                if sec["number"] == sec_num:
                    ex_subs = ex_split_subsections(sec["lines"])
                    raw = "\n".join(ex_subs.get("请求示例", [])).strip()
                    if raw:
                        snippet = raw if len(raw) <= 200 else raw[:200] + " ..."
                        for sl in snippet.splitlines():
                            lines.append(f"    | {sl}")
                    else:
                        lines.append("    | (空)")
                    break
        lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"表格覆盖 {tables_have} / 示例覆盖 {examples_have} / 漏抓 {len(missing)} 条"
    )
    if tag_counter:
        top = ", ".join(f"{k}={v}" for k, v in tag_counter.most_common())
        print(f"原因: {top}")
    print(f"明细: {out}")


if __name__ == "__main__":
    main()
