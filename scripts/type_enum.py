"""扫描 .docx 里所有参数表的"类型"列取值，输出去重+计数的清单。

用途：用这份清单来决定 extract_interfaces.py 里 TYPE_VALUES 白名单该放什么。
不再靠猜或一条条补，数据说话。

识别规则：
- 找到表头（第一行非空）
- 在表头里找标题含 "类型" 的那一列（如 "类型"/"参数类型"/"类 型" 等），其在表里的列序就是"类型列"
- 此后每一行把对应列的值加入计数
- 空行和列数少于类型列索引的行跳过（通常是续行）
- 同时把"参数说明/Description"等**像长中文句子的列**认作描述，不计入

输出按出现次数从多到少排列。短高频 → 真正的类型词；长低频 → 多为续行噪声。

用法:
    python3 scripts/type_enum.py                   # 默认输入
    python3 scripts/type_enum.py <path.docx>
    python3 scripts/type_enum.py <path.docx> 10    # 只看 count >= 10 的
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from extract_interfaces import (  # noqa: E402
    iter_tables,
    split_columns,
    split_sections,
    split_subsections,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"

_TYPE_HEADER_KEYS = ("类型", "参数类型", "类 型")  # 可能的表头关键字


def _find_type_col(header_cols: list[str]) -> int | None:
    for i, col in enumerate(header_cols):
        for key in _TYPE_HEADER_KEYS:
            if key in col:
                return i
    return None


def _process_table(title: str, body: list[str], counts: Counter,
                   samples: dict[str, list[str]]) -> None:
    nonempty = [l for l in body if l.strip()]
    if len(nonempty) < 2:
        return
    header_cols = split_columns(nonempty[0])
    type_col = _find_type_col(header_cols)
    if type_col is None:
        return
    for line in nonempty[1:]:
        cols = split_columns(line)
        if type_col >= len(cols):
            continue  # 续行、列不齐
        val = cols[type_col].strip()
        if not val:
            continue
        counts[val] += 1
        if val not in samples:
            samples[val] = []
        if len(samples[val]) < 3:
            sample = f"{title[:30]} | {cols[0][:40] if cols else ''}"
            samples[val].append(sample)


def main() -> None:
    args = sys.argv[1:]
    path = Path(args[0]) if args and not args[0].isdigit() else DEFAULT_INPUT
    # 可选的最小 count
    min_count = 1
    for a in args:
        if a.isdigit():
            min_count = int(a)

    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    text = read_source(path)
    sections = split_sections(text)

    counts: Counter[str] = Counter()
    samples: dict[str, list[str]] = {}
    table_count = 0
    for sec in sections:
        subs = split_subsections(sec["lines"])
        for marker in ("请求参数", "响应参数"):
            for title, body in iter_tables(subs[marker]):
                _process_table(title, body, counts, samples)
                table_count += 1

    print(f"扫描 {len(sections)} 个 section, {table_count} 张表, "
          f"类型列共 {counts.total()} 次取值, 去重 {len(counts)} 种\n")
    print(f"{'count':>6}  {'type value':<25}  sample (title | col[0])")
    print("-" * 100)
    for val, cnt in counts.most_common():
        if cnt < min_count:
            break
        sample = samples.get(val, [""])[0]
        display_val = val if len(val) <= 25 else val[:22] + "..."
        print(f"{cnt:>6}  {display_val:<25}  {sample}")


if __name__ == "__main__":
    main()
