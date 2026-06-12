"""Convert a Word .docx file to extraction-friendly plain text.

The output format matches the parser input used by this repository:

- paragraphs remain one line each;
- Word heading styles get synthesized numeric prefixes when needed;
- table rows become one line per row, with cells separated by tabs;
- table-of-contents paragraphs are skipped.

Usage:
    python3 scripts/docx_to_text.py data/接口文档.docx
    python3 scripts/docx_to_text.py data/接口文档.docx -o output/接口文档.txt
    python3 scripts/docx_to_text.py data/接口文档.docx -o -
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _docx_utils import read_source


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.extraction.txt")


def convert_docx_to_text(input_path: Path) -> str:
    return read_source(input_path)


def write_docx_text(input_path: Path, output_path: Path | None = None) -> Path:
    final_output = output_path or default_output_path(input_path)
    text = convert_docx_to_text(input_path)
    final_output.parent.mkdir(parents=True, exist_ok=True)
    final_output.write_text(text, encoding="utf-8")
    return final_output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把 Word .docx 转成接口提取用纯文本：段落逐行输出，表格用 Tab 分隔单元格。"
    )
    parser.add_argument("input", type=Path, help="输入 Word .docx 文件")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="输出 .txt 文件；传 '-' 表示写到标准输出。默认 <input>.extraction.txt",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    text = convert_docx_to_text(args.input)

    if str(args.output) == "-":
        sys.stdout.write(text)
        if text and not text.endswith("\n"):
            sys.stdout.write("\n")
        return

    output = args.output or default_output_path(args.input)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"已写出纯文本: {output}")


if __name__ == "__main__":
    main()
