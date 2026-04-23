"""扫描 .docx 所有参数表，列出**指定列**的所有取值及其频次。

跟 type_enum.py 的区别：
- type_enum.py：按"表头含 '类型'"动态定位类型列（列序随表而变，4 列表在 col[1]，
  5/6 列表在 col[2]）
- col_enum.py：按**固定列索引**取值，不管表头叫什么。最适合用来单独分析
  "第二列"（默认 col[1]）实际长什么样，发现表间不一致

用法：
    python3 scripts/col_enum.py                     # 默认扫 col[1]，写 output/col1.txt
    python3 scripts/col_enum.py 2                   # 扫 col[2]
    python3 scripts/col_enum.py 0                   # 扫 col[0]（相当于所有参数名汇总）
    python3 scripts/col_enum.py 1 <input.docx>      # 指定输入文件
    python3 scripts/col_enum.py 1 10                # 只保留 count >= 10 的

输出写到 output/col<idx>.txt (UTF-8)，终端只打摘要——绕开 Windows GBK
对 Word 私用区字符的编码限制。
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from extract_from_tables import (  # noqa: E402
    iter_tables,
    split_columns,
    split_sections,
    split_subsections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def _process_table(
    title: str,
    body: list[str],
    col_idx: int,
    counts: Counter,
    samples: dict[str, str],
) -> None:
    nonempty = [l for l in body if l.strip()]
    if len(nonempty) < 2:
        return
    # nonempty[0] 是表头，跳过；后面每行取 col_idx
    for line in nonempty[1:]:
        cols = split_columns(line)
        if col_idx >= len(cols):
            continue
        val = cols[col_idx].strip()
        if not val:
            continue
        counts[val] += 1
        if val not in samples:
            first_col = cols[0] if cols else ""
            samples[val] = f"{title[:30]} | col[0]={first_col[:30]}"


def _parse_args(argv: list[str]) -> tuple[int, Path, int]:
    col_idx = 1
    min_count = 1
    path: Path | None = None
    # 第一个纯数字参数 → col_idx；第二个纯数字参数 → min_count；
    # 第一个带扩展名/路径分隔符的 → 输入路径
    digit_seen = 0
    for arg in argv:
        if arg.isdigit():
            if digit_seen == 0:
                col_idx = int(arg)
            else:
                min_count = int(arg)
            digit_seen += 1
        else:
            path = Path(arg)
    if path is None:
        path = DEFAULT_INPUT
    return col_idx, path, min_count


def main() -> None:
    col_idx, path, min_count = _parse_args(sys.argv[1:])
    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    text = read_source(path)
    sections = split_sections(text)

    counts: Counter[str] = Counter()
    samples: dict[str, str] = {}
    table_count = 0
    for sec in sections:
        subs = split_subsections(sec["lines"])
        for marker in ("请求参数", "响应参数"):
            for title, body in iter_tables(subs[marker]):
                _process_table(title, body, col_idx, counts, samples)
                table_count += 1

    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = DEFAULT_OUTPUT_DIR / f"col{col_idx}.txt"

    lines: list[str] = []
    lines.append(
        f"扫描 {len(sections)} section / {table_count} 表 / col[{col_idx}] "
        f"共 {counts.total()} 次取值 / 去重 {len(counts)} 种"
    )
    lines.append("")
    lines.append(f"{'count':>6}  {'value':<35}  sample (title | col[0])")
    lines.append("-" * 110)
    for val, cnt in counts.most_common():
        if cnt < min_count:
            break
        display = val if len(val) <= 35 else val[:32] + "..."
        lines.append(f"{cnt:>6}  {display:<35}  {samples.get(val, '')}")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"已扫描 {table_count} 张表，col[{col_idx}] 去重 {len(counts)} 种 -> {out}"
    )


if __name__ == "__main__":
    main()
