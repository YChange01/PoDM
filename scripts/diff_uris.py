"""对比 "表格路径" 和 "示例路径" 两份 interfaces.yaml 的 method+URI，
按 section 对齐，把不一致项分类列出，快速找到文档里写错的请求示例。

用法：
    python3 scripts/diff_uris.py                    # 默认 output/ 下的两份 yaml
    python3 scripts/diff_uris.py <tables.yaml> <examples.yaml>

输出写到 output/uri_diff.txt (UTF-8)，终端只打摘要。

诊断维度：
  - ONLY_IN_TABLES / ONLY_IN_EXAMPLES: 某条 section 在另一边不存在
  - METHOD_DIFF: URI 相同但方法不同
  - NO_LEADING_SLASH: 示例 URI 缺前导 '/' (如 "redfish/v1/...")
  - DOUBLE_SLASH:    示例 URI 中间含 '//' (如 "//redfish/...", ".../Managers//SMN1/...")
  - SPACE_IN_URI:    示例 URI 含空格 (")/" / "/ Actions" 之类)
  - TRUNCATED:       示例 URI 不以 /redfish/v1/ 开头（被截断）
  - MISSING_BRACES:  tables 里是 {xxx}，examples 里填成了具体值 (如 "HDDPlaneDisk1")
  - CASE_DIFF:       其他位置大小写差异 (如 "managers" vs "Managers")
  - PATH_DIFF:       其他路径结构差异（兜底）

依赖：PyYAML 可选，没装就用 json。但 yaml 加载是必须的，为此只能用 PyYAML。
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_STEM = "Atlas PoDManager 1.0.0 Redfish 接口参考_最新"
DEFAULT_TABLES = REPO_ROOT / "output" / f"{DEFAULT_INPUT_STEM}.interfaces.yaml"
DEFAULT_EXAMPLES = REPO_ROOT / "output" / f"{DEFAULT_INPUT_STEM}.example.interfaces.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "output" / "uri_diff.txt"

_BRACE_RE = re.compile(r"\{[^{}]+\}")


def _load_yaml(path: Path) -> dict[str, dict]:
    try:
        import yaml
    except ImportError:
        sys.exit("需要 PyYAML：pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    ifaces = data.get("interfaces", [])
    by_section: dict[str, dict] = {}
    for ifc in ifaces:
        sec = ifc.get("section", "")
        if sec:
            by_section[sec] = ifc
    return by_section


def _diagnose(tables_uri: str, examples_uri: str) -> list[str]:
    """返回示例 URI 相对表格 URI 的问题诊断（可能多条）。"""
    tags: list[str] = []
    e = examples_uri
    if not e.startswith("/"):
        tags.append("NO_LEADING_SLASH")
    # Redfish 是纯路径不会有 http://；URI 里任意位置出现 // 都算 bug
    # （含首部 "//redfish/..." 或中部 ".../Managers//SMN1/..."）
    if "//" in e:
        tags.append("DOUBLE_SLASH")
    if " " in e or "\t" in e:
        tags.append("SPACE_IN_URI")
    # 截断：不以 /redfish/v1/ 或 redfish/v1/ 开头（且有前导 / 已单独报）
    bare = e.lstrip("/")
    if not bare.startswith("redfish/v1/") and not bare.startswith("redfish"):
        tags.append("TRUNCATED")
    # 占位符差异：tables 有 {x}，examples 同位置是具体值
    t_holes = _BRACE_RE.findall(tables_uri)
    e_holes = _BRACE_RE.findall(examples_uri)
    if len(t_holes) > len(e_holes):
        tags.append("MISSING_BRACES")
    # 大小写差异（规范化后相同才算）
    if tables_uri.lower() == examples_uri.lower() and tables_uri != examples_uri:
        tags.append("CASE_DIFF")
    if not tags:
        tags.append("PATH_DIFF")
    return tags


def _fmt_line(iface: dict) -> str:
    m = iface.get("method", "") or ""
    u = iface.get("uri", "") or ""
    return f"[{m}] {u}" if m else u


def main() -> None:
    args = sys.argv[1:]
    tables_path = Path(args[0]) if len(args) >= 1 else DEFAULT_TABLES
    examples_path = Path(args[1]) if len(args) >= 2 else DEFAULT_EXAMPLES

    for p in (tables_path, examples_path):
        if not p.exists():
            sys.exit(f"输入不存在: {p}")

    t = _load_yaml(tables_path)
    e = _load_yaml(examples_path)

    t_only = sorted(set(t) - set(e), key=lambda s: tuple(int(x) for x in s.split(".") if x.isdigit()))
    e_only = sorted(set(e) - set(t), key=lambda s: tuple(int(x) for x in s.split(".") if x.isdigit()))
    common = sorted(set(t) & set(e), key=lambda s: tuple(int(x) for x in s.split(".") if x.isdigit()))

    identical: list[str] = []
    diffs: list[tuple[str, dict, dict, list[str]]] = []
    method_only_diff: list[tuple[str, dict, dict]] = []

    for sec in common:
        ti, ei = t[sec], e[sec]
        t_method = (ti.get("method") or "").upper()
        e_method = (ei.get("method") or "").upper()
        t_uri = ti.get("uri") or ""
        e_uri = ei.get("uri") or ""
        if t_method == e_method and t_uri == e_uri:
            identical.append(sec)
        elif t_uri == e_uri and t_method != e_method:
            method_only_diff.append((sec, ti, ei))
        else:
            tags = _diagnose(t_uri, e_uri)
            if t_method != e_method:
                tags.append("METHOD_DIFF")
            diffs.append((sec, ti, ei, tags))

    # 计数
    tag_counter: Counter[str] = Counter()
    for _sec, _ti, _ei, tags in diffs:
        tag_counter.update(tags)

    # 渲染报告
    lines: list[str] = []
    lines.append(f"tables:   {tables_path}")
    lines.append(f"examples: {examples_path}")
    lines.append("")
    lines.append(
        f"表格路径 {len(t)} 条 / 示例路径 {len(e)} 条 / 共同 section {len(common)} 条"
    )
    lines.append(
        f"  完全一致:      {len(identical):>4}"
    )
    lines.append(
        f"  只在表格里:    {len(t_only):>4}"
    )
    lines.append(
        f"  只在示例里:    {len(e_only):>4}"
    )
    lines.append(
        f"  URI 不一致:    {len(diffs):>4}"
    )
    lines.append(
        f"  仅 method 不同:{len(method_only_diff):>4}"
    )
    lines.append("")
    if tag_counter:
        lines.append("不一致原因分布：")
        for tag, cnt in tag_counter.most_common():
            lines.append(f"  {tag:<20} {cnt}")
        lines.append("")

    # 明细
    if t_only:
        lines.append(f"## 只在表格路径里 ({len(t_only)} 条)")
        for sec in t_only:
            lines.append(f"  {sec}  {t[sec].get('title','')}  {_fmt_line(t[sec])}")
        lines.append("")
    if e_only:
        lines.append(f"## 只在示例路径里 ({len(e_only)} 条)")
        for sec in e_only:
            lines.append(f"  {sec}  {e[sec].get('title','')}  {_fmt_line(e[sec])}")
        lines.append("")
    if method_only_diff:
        lines.append(f"## URI 相同、方法不同 ({len(method_only_diff)} 条)")
        for sec, ti, ei in method_only_diff:
            lines.append(f"  {sec}  {ti.get('title','')}")
            lines.append(f"    tables:   [{ti.get('method','')}] {ti.get('uri','')}")
            lines.append(f"    examples: [{ei.get('method','')}] {ei.get('uri','')}")
        lines.append("")
    if diffs:
        lines.append(f"## URI 不一致 ({len(diffs)} 条)")
        for sec, ti, ei, tags in diffs:
            lines.append(f"  {sec}  {ti.get('title','')}  [{','.join(tags)}]")
            lines.append(f"    tables:   {_fmt_line(ti)}")
            lines.append(f"    examples: {_fmt_line(ei)}")
        lines.append("")

    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 终端摘要
    print(
        f"对比完成：表格 {len(t)} / 示例 {len(e)} / 共同 {len(common)}"
    )
    print(
        f"  一致 {len(identical)} / URI 不一致 {len(diffs)} / "
        f"仅方法不同 {len(method_only_diff)} / 只在表格 {len(t_only)} / 只在示例 {len(e_only)}"
    )
    if tag_counter:
        top = ", ".join(f"{k}={v}" for k, v in tag_counter.most_common(5))
        print(f"  top 原因: {top}")
    print(f"明细写到: {DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
