#!/usr/bin/env python3
"""Extract CMCC document headings into a standalone table of contents."""
from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cmcc_docx_utils import read_source  # noqa: E402
from _yaml_io import dump_yaml  # noqa: E402
from extract_cmcc import DEFAULT_INPUT, normalize_source_text, parse_heading_title  # noqa: E402


DEFAULT_OUTPUT = Path("output/20260610/cmcc.toc.yaml")


@dataclass
class TocEntry:
    index: int
    section: str
    level: int
    title: str
    line: int


def extract_toc(text: str) -> list[TocEntry]:
    entries: list[TocEntry] = []
    seen: set[tuple[str, str]] = set()
    for line_number, line in enumerate(normalize_source_text(text).splitlines(), start=1):
        section, title = parse_heading_title(line)
        if not section or not title:
            continue
        key = (section, title)
        if key in seen:
            continue
        seen.add(key)
        entries.append(
            TocEntry(
                index=len(entries) + 1,
                section=section,
                level=section.count(".") + 1,
                title=title,
                line=line_number,
            )
        )
    return entries


def write_toc_text(entries: list[TocEntry], output_path: Path) -> Path:
    text_path = output_path.with_suffix(".txt")
    text_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"{entry.index}\t{entry.section}\t{entry.level}\t{entry.title}\tline:{entry.line}"
        for entry in entries
    ]
    text_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return text_path


def resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if argv:
        input_path = Path(argv[0])
        output_path = Path(argv[1]) if len(argv) > 1 else input_path.with_suffix(".toc.yaml")
        return input_path, output_path
    return DEFAULT_INPUT, DEFAULT_OUTPUT


def main(argv: list[str] | None = None) -> None:
    input_path, output_path = resolve_io(sys.argv[1:] if argv is None else argv)
    if not input_path.exists():
        raise SystemExit(f"输入文件不存在: {input_path}")

    entries = extract_toc(read_source(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path = dump_yaml({"toc": [asdict(entry) for entry in entries]}, output_path)
    text_path = write_toc_text(entries, output_path)
    print(f"已提取 {len(entries)} 条 CMCC 目录")
    print(f"  YAML: {yaml_path}")
    print(f"  TXT:  {text_path}")


if __name__ == "__main__":
    main()
