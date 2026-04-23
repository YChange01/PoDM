#!/usr/bin/env python3
"""Compare Redfish endpoints between BMC.txt and PoDM.txt."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BMC = ROOT / "data" / "BMC.txt"
PODM = ROOT / "data" / "PoDM.txt"


def normalize(line: str) -> str:
    s = line.strip()
    if not s:
        return ""
    # ensure leading slash
    if not s.startswith("/"):
        s = "/" + s
    # collapse whitespace inside URL
    s = re.sub(r"\s+", "", s)
    # unify placeholder syntax: {foo} -> foo
    s = s.replace("{", "").replace("}", "")
    # unify Oem/Huawei/Public/ vs Oem/Huawei/
    s = s.replace("/Oem/Huawei/Public/", "/Oem/Huawei/")
    # collapse double slashes
    s = re.sub(r"/+", "/", s)
    # drop trailing slash
    if len(s) > 1 and s.endswith("/"):
        s = s[:-1]
    # case-normalize path segments for comparison robustness
    return s.lower()


def load(path: Path):
    raw_lines = [l for l in path.read_text().splitlines() if l.strip()]
    norm = set()
    for l in raw_lines:
        n = normalize(l)
        if n:
            norm.add(n)
    return raw_lines, norm


def short_category(endpoint: str) -> str:
    parts = endpoint.split("/")
    # parts[0]="" parts[1]="redfish" parts[2]="v1" parts[3]=category
    if len(parts) >= 4:
        return parts[3]
    return "(root)"


def main():
    bmc_raw, bmc = load(BMC)
    podm_raw, podm = load(PODM)

    common = bmc & podm
    only_bmc = bmc - podm
    only_podm = podm - bmc

    print(f"BMC  总行数: {len(bmc_raw)}  去重规范化后: {len(bmc)}")
    print(f"PoDM 总行数: {len(podm_raw)}  去重规范化后: {len(podm)}")
    print()
    print(f"共同接口  : {len(common)}")
    print(f"仅 BMC 有 : {len(only_bmc)}")
    print(f"仅 PoDM 有: {len(only_podm)}")
    print()

    # Category summary
    def by_cat(s):
        d = {}
        for e in s:
            d.setdefault(short_category(e), []).append(e)
        return d

    cat_only_bmc = by_cat(only_bmc)
    cat_only_podm = by_cat(only_podm)
    cat_common = by_cat(common)

    all_cats = sorted(set(cat_only_bmc) | set(cat_only_podm) | set(cat_common))
    print("=" * 92)
    print(f"{'分类':<24} {'共同':>6} {'仅BMC':>8} {'仅PoDM':>8}")
    print("-" * 92)
    for c in all_cats:
        print(f"{c:<24} {len(cat_common.get(c, [])):>6} {len(cat_only_bmc.get(c, [])):>8} {len(cat_only_podm.get(c, [])):>8}")
    print("=" * 92)
    print()

    print("## 仅 BMC 有的接口（按分类）")
    for c in sorted(cat_only_bmc):
        print(f"\n### [{c}]  ({len(cat_only_bmc[c])})")
        for e in sorted(cat_only_bmc[c]):
            print(f"  - {e}")

    print("\n\n## 仅 PoDM 有的接口（按分类）")
    for c in sorted(cat_only_podm):
        print(f"\n### [{c}]  ({len(cat_only_podm[c])})")
        for e in sorted(cat_only_podm[c]):
            print(f"  - {e}")


if __name__ == "__main__":
    main()
