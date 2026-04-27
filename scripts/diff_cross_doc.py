"""跨文档接口对比：BMC iBMC300 vs PoDManager。

输出 markdown 报告 (analysis/cross_doc_diff.md)，包含：
- 总览统计
- 共有接口的 method / URI / 各类参数差异
- 仅 BMC 接口（PoDM 缺失）
- 仅 PoDM 接口（BMC 缺失）
- 给 PoDM 文档的修订建议（基于 BMC 的差异）

匹配策略：
1. 先按 **标题精确匹配** 配对
2. 再按 **归一化 URI 匹配**（剥 scheme://host、bare 占位符加 {}）兜底
3. 共有接口取并集，标记匹配途径

用法：
    python3 scripts/diff_cross_doc.py
    python3 scripts/diff_cross_doc.py <bmc.yaml> <podm.yaml>

默认输入：output/ 下两份 yaml；输出写到 analysis/cross_doc_diff.md。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from collections import Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BMC = REPO_ROOT / "output" / "华为服务器 iBMC300 Redfish 接口说明_最新.bmc.interfaces.yaml"
DEFAULT_PODM = REPO_ROOT / "output" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.interfaces.yaml"
DEFAULT_OUT = REPO_ROOT / "analysis" / "cross_doc_diff.md"

CATS = ("path", "header", "body", "query", "response")
PATH_KEYWORDS = {"redfish", "v1", "actions", "oem", "huawei", "public"}
_PLACEHOLDER_RE = re.compile(r"^[a-z][a-z_0-9]*$")


# =================== URI 归一化 ===================

def normalize_uri(uri: str) -> str:
    """归一化两份 doc 的 URI 到可比较的形式：
    - 去 scheme://host (BMC 的 https://device_ip → 空)
    - bare 小写下划线占位符加 {} (BMC 用 manager_id, PoDM 用 {manager_id})
    - 去 query string
    - 末尾去多余 /
    """
    if not uri:
        return ""
    uri = re.sub(r"^https?://[^/]+", "", uri)
    uri = uri.split("?", 1)[0]
    parts = []
    for seg in uri.split("/"):
        if not seg:
            parts.append("")
            continue
        if seg.startswith("{") and seg.endswith("}"):
            parts.append(seg)
            continue
        if _PLACEHOLDER_RE.match(seg) and seg.lower() not in PATH_KEYWORDS:
            parts.append("{" + seg + "}")
            continue
        parts.append(seg)
    out = "/".join(parts)
    while out.endswith("/") and out != "/":
        out = out[:-1]
    return out


def normalize_uri_anonymous(uri: str) -> str:
    """更激进归一化：把所有 {xxx} 都替换成 {}, 仅留路径结构。
    用于"路径相同但占位符不同"的近似匹配。
    """
    n = normalize_uri(uri)
    return re.sub(r"\{[^{}]+\}", "{}", n)


# =================== 加载与配对 ===================

def load(path: Path) -> list[dict]:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))["interfaces"]


def index_by(items: list[dict], key_fn) -> dict[str, dict]:
    """按 key_fn(item) 索引；冲突时保留较后一条。"""
    out: dict[str, dict] = {}
    for it in items:
        k = key_fn(it)
        if k:
            out[k] = it
    return out


def pair_interfaces(podm: list[dict], bmc: list[dict]) -> tuple[list, list, list]:
    """配对，返回 (matched, only_podm, only_bmc)。
    matched = [(podm_iface, bmc_iface, match_via)]

    四遍配对，前一轮成功的就不参与后续：
      pass 1: 标题精确（title 唯一最强信号）
      pass 2: 归一化 URI + method 联合（避免把 GET 配到 PATCH 上）
      pass 3: 归一化 URI 单独（method 不一致也接受）
      pass 4: URI 路径骨架（占位符匿名化兜底）
    """
    used_p: set[str] = set()
    used_b: set[int] = set()
    matched: list[tuple[dict, dict, str]] = []

    def try_match(key_fn_p, key_fn_b, via: str) -> None:
        # 用 list 保留所有冲突候选；按 section 顺序取第一个未用的
        idx_p: dict = {}
        for x in podm:
            if x["section"] in used_p:
                continue
            k = key_fn_p(x)
            if k:
                idx_p.setdefault(k, []).append(x)
        for b in bmc:
            if id(b) in used_b:
                continue
            k = key_fn_b(b)
            if not k:
                continue
            for p in idx_p.get(k, []):
                if p["section"] not in used_p:
                    matched.append((p, b, via))
                    used_p.add(p["section"])
                    used_b.add(id(b))
                    break

    try_match(lambda x: x["title"],
              lambda x: x["title"],
              "title")
    try_match(lambda x: (normalize_uri(x["uri"]), x.get("method", "")),
              lambda x: (normalize_uri(x["uri"]), x.get("method", "")),
              "uri+method")
    try_match(lambda x: normalize_uri(x["uri"]),
              lambda x: normalize_uri(x["uri"]),
              "uri")
    try_match(lambda x: normalize_uri_anonymous(x["uri"]),
              lambda x: normalize_uri_anonymous(x["uri"]),
              "uri-skeleton")

    only_podm = [p for p in podm if p["section"] not in used_p]
    only_bmc = [b for b in bmc if id(b) not in used_b]
    return matched, only_podm, only_bmc


# =================== 参数集合 diff ===================

def diff_params(podm_iface: dict, bmc_iface: dict) -> dict:
    """返回 {cat: {only_podm, only_bmc, common}} per category."""
    out = {}
    for c in CATS:
        p_set = set(podm_iface["params"].get(c) or [])
        b_set = set(bmc_iface["params"].get(c) or [])
        out[c] = {
            "only_podm": sorted(p_set - b_set),
            "only_bmc": sorted(b_set - p_set),
            "common": sorted(p_set & b_set),
        }
    return out


def has_diff(d: dict) -> bool:
    return any(d[c]["only_podm"] or d[c]["only_bmc"] for c in CATS)


# =================== 报告渲染 ===================

def render_report(podm: list[dict], bmc: list[dict],
                  matched: list, only_podm: list, only_bmc: list) -> str:
    lines: list[str] = []
    lines.append("# BMC vs PoDManager 跨文档对比报告\n")

    # ---- 总览 ----
    lines.append("## 总览\n")
    via_counter = Counter(via for _, _, via in matched)
    method_diff = sum(1 for p, b, _ in matched if (p["method"] or "") != (b["method"] or ""))
    uri_diff = sum(1 for p, b, _ in matched
                   if normalize_uri(p["uri"]) != normalize_uri(b["uri"]))
    param_diff = sum(1 for p, b, _ in matched if has_diff(diff_params(p, b)))

    lines.append(f"| 维度 | 数值 |")
    lines.append(f"|---|---:|")
    lines.append(f"| PoDManager 接口数 | {len(podm)} |")
    lines.append(f"| BMC 接口数 | {len(bmc)} |")
    lines.append(f"| 配对成功（共有接口）| **{len(matched)}** |")
    lines.append(f"|  ├ 通过标题精确配对 | {via_counter['title']} |")
    lines.append(f"|  ├ 通过 URI+method 配对 | {via_counter['uri+method']} |")
    lines.append(f"|  ├ 通过归一化 URI 配对 | {via_counter['uri']} |")
    lines.append(f"|  └ 通过路径骨架配对 | {via_counter['uri-skeleton']} |")
    lines.append(f"| 仅 PoDManager（PoDM 独有）| {len(only_podm)} |")
    lines.append(f"| 仅 BMC（BMC 独有）| {len(only_bmc)} |")
    lines.append(f"| 共有接口中 method 不一致 | {method_diff} |")
    lines.append(f"| 共有接口中归一化 URI 不一致 | {uri_diff} |")
    lines.append(f"| 共有接口中参数集合有差异 | {param_diff} |\n")

    # ---- 共有接口 method/URI 不一致 ----
    method_mismatches = [(p, b, via) for p, b, via in matched
                          if (p["method"] or "") != (b["method"] or "")]
    if method_mismatches:
        lines.append(f"## 共有接口：method 不一致（{len(method_mismatches)} 条）\n")
        lines.append(f"| PoDM section | 标题 | PoDM | BMC |")
        lines.append(f"|---|---|---|---|")
        for p, b, _ in method_mismatches:
            lines.append(f"| {p['section']} | {p['title']} | `{p['method']}` | `{b['method']}` |")
        lines.append("")

    uri_mismatches = [(p, b, via) for p, b, via in matched
                      if normalize_uri(p["uri"]) != normalize_uri(b["uri"])]
    if uri_mismatches:
        lines.append(f"## 共有接口：归一化 URI 不一致（{len(uri_mismatches)} 条）\n")
        lines.append("> 已经统一归一化（剥 https://device_ip + bare 占位符加 {}）后仍不同。\n")
        lines.append(f"| section | 标题 | PoDM URI | BMC URI |")
        lines.append(f"|---|---|---|---|")
        for p, b, _ in uri_mismatches[:50]:
            lines.append(f"| {p['section']} | {p['title'][:30]} | `{normalize_uri(p['uri'])[:60]}` | `{normalize_uri(b['uri'])[:60]}` |")
        if len(uri_mismatches) > 50:
            lines.append(f"\n... 还有 {len(uri_mismatches)-50} 条")
        lines.append("")

    # ---- 共有接口参数差异统计 ----
    lines.append("## 共有接口参数差异（按类别）\n")
    cat_stat: dict[str, Counter[str]] = {c: Counter() for c in CATS}
    diff_records: list[tuple[int, dict, dict, dict]] = []  # (total_diff, p, b, d)
    for p, b, _ in matched:
        d = diff_params(p, b)
        total = sum(len(d[c]["only_podm"]) + len(d[c]["only_bmc"]) for c in CATS)
        if total > 0:
            diff_records.append((total, p, b, d))
        for c in CATS:
            if d[c]["only_podm"]:
                cat_stat[c]["only_podm_sections"] += 1
                cat_stat[c]["only_podm_total"] += len(d[c]["only_podm"])
            if d[c]["only_bmc"]:
                cat_stat[c]["only_bmc_sections"] += 1
                cat_stat[c]["only_bmc_total"] += len(d[c]["only_bmc"])
    lines.append(f"| 类别 | 仅 PoDM 字段(接口数 / 字段总数) | 仅 BMC 字段(接口数 / 字段总数) |")
    lines.append(f"|---|---:|---:|")
    for c in CATS:
        cs = cat_stat[c]
        lines.append(f"| {c} | {cs['only_podm_sections']} 接口 / {cs['only_podm_total']} 字段 | {cs['only_bmc_sections']} 接口 / {cs['only_bmc_total']} 字段 |")
    lines.append("")

    # ---- 共有接口参数差异 详细 ----
    diff_records.sort(key=lambda x: -x[0])
    lines.append(f"## 共有接口参数差异 详细列表（共 {len(diff_records)} 条，按差异字段总数降序）\n")
    lines.append("> 每条接口列出每个类别下「仅 PoDM 有」和「仅 BMC 有」的字段。空类别省略。\n")

    def join_fields(items: list[str]) -> str:
        return ", ".join(f"`{x}`" for x in items) if items else "—"

    for total, p, b, d in diff_records:
        method_p = p.get("method") or "?"
        method_b = b.get("method") or "?"
        method_tag = f"`{method_p}`" if method_p == method_b else f"PoDM `{method_p}` / BMC `{method_b}`"
        lines.append(f"### {p['section']} {p['title']}（差异 {total}）\n")
        lines.append(f"- BMC section: `{b['section']}`  method: {method_tag}")
        lines.append(f"- PoDM URI: `{normalize_uri(p['uri'])}`")
        if normalize_uri(p["uri"]) != normalize_uri(b["uri"]):
            lines.append(f"- BMC URI: `{normalize_uri(b['uri'])}`  ← URI 不一致")
        lines.append("")
        lines.append(f"| 类别 | 仅 PoDM | 仅 BMC |")
        lines.append(f"|---|---|---|")
        for c in CATS:
            op = d[c]["only_podm"]
            ob = d[c]["only_bmc"]
            if not op and not ob:
                continue
            lines.append(f"| {c} | {join_fields(op)} | {join_fields(ob)} |")
        lines.append("")

    # ---- PoDM 改进建议（按 response 字段缺失全量列出）----
    lines.append("## PoDManager 修订建议（按 BMC response 字段补充优先级）\n")
    lines.append("> 列出所有 BMC 同名接口的 response 字段集合中、PoDM 没列出的字段。"
                  "BMC 那边大多是真实响应数据，PoDM 漏列的字段大概率是 schema 表写漏。"
                  "按缺失字段数降序。\n")

    suggestions = []
    for p, b, _ in matched:
        d = diff_params(p, b)
        bmc_extra_resp = d["response"]["only_bmc"]
        if bmc_extra_resp:
            suggestions.append((len(bmc_extra_resp), p, b, bmc_extra_resp))
    suggestions.sort(key=lambda x: -x[0])

    lines.append(f"### 全量 {len(suggestions)} 条（PoDM response 比 BMC 缺字段的接口）\n")
    lines.append(f"| PoDM section | 标题 | 缺失数 | BMC 多出的 response 字段 |")
    lines.append(f"|---|---|---:|---|")
    for n, p, _, extras in suggestions:
        cells = ", ".join(f"`{x}`" for x in extras)
        lines.append(f"| {p['section']} | {p['title']} | {n} | {cells} |")
    lines.append("")

    # ---- 仅 PoDM 接口 ----
    lines.append(f"## 仅 PoDManager 有 / BMC 无（{len(only_podm)} 条）\n")
    lines.append("> 这些接口可能是 PoDM 特有，或 BMC 用了不同的标题 / URI 没匹配上。建议人工核对一遍。\n")
    if only_podm:
        lines.append(f"| section | method | 标题 | URI |")
        lines.append(f"|---|---|---|---|")
        for p in sorted(only_podm, key=lambda x: x["section"]):
            lines.append(f"| {p['section']} | {p['method']} | {p['title']} | `{normalize_uri(p['uri'])[:60]}` |")
    lines.append("")

    # ---- 仅 BMC 接口 ----
    lines.append(f"## 仅 BMC 有 / PoDManager 无（{len(only_bmc)} 条）\n")
    lines.append("> 这些是 BMC 比 PoDM 多的接口。如 PoDM 有相关功能但用了不同接口名/URI，可考虑对齐 BMC 命名。\n")
    if only_bmc:
        lines.append(f"| section | method | 标题 | URI |")
        lines.append(f"|---|---|---|---|")
        for b in sorted(only_bmc, key=lambda x: x["section"]):
            lines.append(f"| {b['section']} | {b['method']} | {b['title']} | `{normalize_uri(b['uri'])[:60]}` |")
    lines.append("")

    return "\n".join(lines) + "\n"


# =================== 入口 ===================

def main() -> None:
    args = sys.argv[1:]
    bmc_path = Path(args[0]) if len(args) >= 1 else DEFAULT_BMC
    podm_path = Path(args[1]) if len(args) >= 2 else DEFAULT_PODM
    out_path = Path(args[2]) if len(args) >= 3 else DEFAULT_OUT

    if not bmc_path.exists():
        sys.exit(f"BMC yaml 不存在: {bmc_path}")
    if not podm_path.exists():
        sys.exit(f"PoDM yaml 不存在: {podm_path}")

    podm = load(podm_path)
    bmc = load(bmc_path)
    matched, only_podm, only_bmc = pair_interfaces(podm, bmc)
    report = render_report(podm, bmc, matched, only_podm, only_bmc)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print(f"对比完成：")
    print(f"  PoDM 接口  : {len(podm)}")
    print(f"  BMC  接口  : {len(bmc)}")
    print(f"  共有 (配对): {len(matched)}")
    print(f"  仅 PoDM    : {len(only_podm)}")
    print(f"  仅 BMC     : {len(only_bmc)}")
    print(f"  报告写到   : {out_path}")


if __name__ == "__main__":
    main()
