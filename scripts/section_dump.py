"""打印指定 section 经 read_source 展开后的原始文本——用于排查表格解析失败。

制表符会以可见的 \\t 形式显示，便于看清表格列到底怎么分隔。

用法:
    python3 scripts/section_dump.py 4.2.25
    python3 scripts/section_dump.py 4.2.25 <其他.docx>

依赖：仅 Python 3 标准库。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"

_HEADING = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+")


def _visible(line: str) -> str:
    return line.replace("\t", r"\t")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: section_dump.py <section_number> [input.docx]")
        sys.exit(1)
    target = sys.argv[1].strip()
    inp = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_INPUT
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    text = read_source(inp)
    in_section = False
    captured = 0
    for line in text.splitlines():
        match = _HEADING.match(line)
        if match:
            num = match.group(1)
            if num == target:
                print(f"========== {line.strip()} ==========")
                in_section = True
                continue
            if in_section:
                # 进入下一节，停
                break
        if in_section:
            print(_visible(line))
            captured += 1
            if captured > 400:
                print("... [truncated at 400 lines] ...")
                break

    if not in_section:
        sys.exit(f"没找到章节 {target}")


if __name__ == "__main__":
    main()
