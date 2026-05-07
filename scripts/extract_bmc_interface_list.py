#!/usr/bin/env python3
"""提取 BMC 接口清单，输出 index/section/title/method/uri YAML。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _defaults import BMC_DOCX, BMC_STEM, OUTPUT_DIR  # noqa: E402
from _docx_utils import read_source  # noqa: E402
from _interface_list import InterfaceSummary, write_interface_list_yaml  # noqa: E402
from extract_bmc import (  # noqa: E402
    is_interface_section,
    parse_command_format,
    split_sections_chapter3,
    split_subsections_bmc,
)

DEFAULT_INPUT = BMC_DOCX
DEFAULT_OUTPUT = OUTPUT_DIR / f"{BMC_STEM}.interface-list.yaml"


def extract(text: str) -> list[InterfaceSummary]:
    out: list[InterfaceSummary] = []
    for sec in split_sections_chapter3(text):
        if not is_interface_section(sec):
            continue
        subs = split_subsections_bmc(sec["lines"])
        cmd = parse_command_format(subs.get("命令格式", []))
        if not cmd["url"]:
            continue
        out.append(
            InterfaceSummary(
                section=sec["number"],
                title=sec["title"],
                method=cmd["method"],
                uri=cmd["url"],
            )
        )
    return out


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        inp = Path(argv[1])
        out = Path(argv[2]) if len(argv) > 2 else inp.with_suffix(".interface-list.yaml")
        return inp, out
    return DEFAULT_INPUT, DEFAULT_OUTPUT


def main() -> None:
    inp, out = _resolve_io(sys.argv)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    interfaces = extract(read_source(inp))
    write_interface_list_yaml(interfaces, out)
    print(f"已提取 {len(interfaces)} 个 BMC 接口 -> {out}")


if __name__ == "__main__":
    main()
