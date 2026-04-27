"""对比 "表格 yaml" 和 "示例 yaml" 的参数差异，按 section + category 输出。

跟 diff_uris.py 的关系：
  - diff_uris.py     : 只看每个接口的 method+URI 是否一致（路径层面的 doc bug）
  - diff_params.py   : 同一个接口下，path/header/body/query/response 五类参数集合是否一致
                       （参数层面的 doc bug：表格列了示例没发，或示例发了表格漏列）

用法：
    python3 scripts/diff_params.py
    python3 scripts/diff_params.py <tables.yaml> <examples.yaml>

默认输入：
    output/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.interfaces.yaml
    output/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.example.interfaces.yaml
默认输出：
    output/param_diff.txt   (UTF-8，完整明细)
stdout 只打摘要，避免 Windows GBK 控制台出错。

诊断维度（每个 section、每个 category 独立计数）：
  - ONLY_IN_TABLES       : 表格列了，示例没出现
  - ONLY_IN_EXAMPLES     : 示例出现，表格没列
  - ORDER_DIFF           : 集合相同但顺序不同（仅提示，不算 doc bug）
  - 完全一致的 category 不进明细，只入计数

依赖：PyYAML（必需，因为要读 yaml）。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT_STEM = "Atlas PoDManager 1.0.0 Redfish 接口参考_最新"
DEFAULT_TABLES = REPO_ROOT / "output" / f"{DEFAULT_INPUT_STEM}.interfaces.yaml"
DEFAULT_EXAMPLES = REPO_ROOT / "output" / f"{DEFAULT_INPUT_STEM}.example.interfaces.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "output" / "param_diff.txt"

CATEGORIES = ("path", "header", "body", "query", "response")


def _load_yaml(path: Path) -> dict[str, dict]:
    try:
        import yaml
    except ImportError:
        sys.exit("需要 PyYAML：pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    out: dict[str, dict] = {}
    for ifc in data.get("interfaces", []):
        sec = ifc.get("section", "")
        if sec:
            out[sec] = ifc
    return out


def _params_of(iface: dict, cat: str) -> list[str]:
    p = iface.get("params") or {}
    val = p.get(cat) or []
    return [str(x) for x in val]


def _section_key(s: str) -> tuple:
    return tuple(int(x) if x.isdigit() else x for x in s.split("."))


def _diff_one(t_list: list[str], e_list: list[str]) -> dict:
    """返回该 category 的差异统计：only_t / only_e / order_diff。"""
    t_set, e_set = set(t_list), set(e_list)
    only_t = [x for x in t_list if x not in e_set]
    only_e = [x for x in e_list if x not in t_set]
    same_set = t_set == e_set
    order_diff = same_set and t_list != e_list
    return {
        "only_t": only_t,
        "only_e": only_e,
        "order_diff": order_diff,
        "identical": same_set and not order_diff,
    }


def main() -> None:
    args = sys.argv[1:]
    tables_path = Path(args[0]) if len(args) >= 1 else DEFAULT_TABLES
    examples_path = Path(args[1]) if len(args) >= 2 else DEFAULT_EXAMPLES

    for p in (tables_path, examples_path):
        if not p.exists():
            sys.exit(f"输入不存在: {p}")

    t = _load_yaml(tables_path)
    e = _load_yaml(examples_path)

    common = sorted(set(t) & set(e), key=_section_key)
    t_only_secs = sorted(set(t) - set(e), key=_section_key)
    e_only_secs = sorted(set(e) - set(t), key=_section_key)

    # 按 section 收集差异
    per_section: list[tuple[str, dict[str, dict]]] = []
    cat_stats: dict[str, Counter[str]] = {c: Counter() for c in CATEGORIES}
    sections_with_any_diff: list[str] = []

    for sec in common:
        sec_diff: dict[str, dict] = {}
        any_diff = False
        for cat in CATEGORIES:
            d = _diff_one(_params_of(t[sec], cat), _params_of(e[sec], cat))
            sec_diff[cat] = d
            if d["identical"]:
                cat_stats[cat]["identical"] += 1
            else:
                if d["only_t"]:
                    cat_stats[cat]["only_in_tables"] += 1
                if d["only_e"]:
                    cat_stats[cat]["only_in_examples"] += 1
                if d["order_diff"]:
                    cat_stats[cat]["order_diff"] += 1
                any_diff = True
        if any_diff:
            sections_with_any_diff.append(sec)
        per_section.append((sec, sec_diff))

    # 渲染报告
    lines: list[str] = []
    lines.append(f"tables:   {tables_path}")
    lines.append(f"examples: {examples_path}")
    lines.append("")
    lines.append(
        f"表格接口 {len(t)} 条 / 示例接口 {len(e)} 条 / 共同 section {len(common)} 条"
    )
    lines.append(f"  共同 section 中、参数完全一致:  {len(common) - len(sections_with_any_diff)}")
    lines.append(f"  共同 section 中、参数有差异:    {len(sections_with_any_diff)}")
    lines.append(f"  只在表格里的 section:          {len(t_only_secs)}")
    lines.append(f"  只在示例里的 section:          {len(e_only_secs)}")
    lines.append("")

    lines.append("各类别差异统计 (基于 共同 section)：")
    lines.append(
        f"  {'category':<10} {'identical':>10} {'only_tables':>12} {'only_examples':>14} {'order_diff':>11}"
    )
    for cat in CATEGORIES:
        c = cat_stats[cat]
        lines.append(
            f"  {cat:<10} {c['identical']:>10} {c['only_in_tables']:>12} "
            f"{c['only_in_examples']:>14} {c['order_diff']:>11}"
        )
    lines.append("")

    if t_only_secs:
        lines.append(f"## 只在表格 yaml 里的 section ({len(t_only_secs)} 条)")
        for sec in t_only_secs:
            lines.append(f"  {sec}  {t[sec].get('title','')}")
        lines.append("")
    if e_only_secs:
        lines.append(f"## 只在示例 yaml 里的 section ({len(e_only_secs)} 条)")
        for sec in e_only_secs:
            lines.append(f"  {sec}  {e[sec].get('title','')}")
        lines.append("")

    if sections_with_any_diff:
        lines.append(f"## 参数有差异的 section 明细 ({len(sections_with_any_diff)} 条)")
        for sec, sec_diff in per_section:
            if sec not in set(sections_with_any_diff):
                continue
            title = t[sec].get("title", "") or e[sec].get("title", "")
            lines.append(f"  {sec}  {title}")
            for cat in CATEGORIES:
                d = sec_diff[cat]
                if d["identical"]:
                    continue
                tag_bits: list[str] = []
                if d["only_t"]:
                    tag_bits.append(f"only_tables={len(d['only_t'])}")
                if d["only_e"]:
                    tag_bits.append(f"only_examples={len(d['only_e'])}")
                if d["order_diff"]:
                    tag_bits.append("order_diff")
                lines.append(f"    [{cat}] {' '.join(tag_bits)}")
                if d["only_t"]:
                    lines.append(f"      only_tables  : {d['only_t']}")
                if d["only_e"]:
                    lines.append(f"      only_examples: {d['only_e']}")
        lines.append("")

    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # stdout 摘要
    print(
        f"对比完成：表格 {len(t)} / 示例 {len(e)} / 共同 {len(common)} / "
        f"参数有差异 {len(sections_with_any_diff)}"
    )
    print(
        f"  只在表格 section: {len(t_only_secs)}  /  只在示例 section: {len(e_only_secs)}"
    )
    for cat in CATEGORIES:
        c = cat_stats[cat]
        bits = []
        if c["only_in_tables"]:
            bits.append(f"only_tables={c['only_in_tables']}")
        if c["only_in_examples"]:
            bits.append(f"only_examples={c['only_in_examples']}")
        if c["order_diff"]:
            bits.append(f"order_diff={c['order_diff']}")
        tail = " | ".join(bits) if bits else "all identical"
        print(f"  [{cat:<8}] identical={c['identical']:>3}  {tail}")
    print(f"明细写到: {DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
