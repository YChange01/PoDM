#!/usr/bin/env python3
"""提取 PoDManager 接口清单，输出 index/section/title/method/uri YAML。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _defaults import OUTPUT_DIR, PODM_DOCX, PODM_STEM  # noqa: E402
from _doc_structure import (  # noqa: E402
    dedup_sections,
    section_has_uri,
    split_sections,
    split_subsections,
)
from _docx_utils import read_source  # noqa: E402
from _interface_list import (  # noqa: E402
    InterfaceSummary,
    first_non_empty,
    write_interface_list_yaml,
)

DEFAULT_INPUT = PODM_DOCX
DEFAULT_OUTPUT = OUTPUT_DIR / f"{PODM_STEM}.interface-list.yaml"


def extract(text: str) -> list[InterfaceSummary]:
    out: list[InterfaceSummary] = []
    for sec in dedup_sections(split_sections(text)):
        if not section_has_uri(sec):
            continue
        subs = split_subsections(sec["lines"])
        uri = first_non_empty(subs["URI"])
        if not uri:
            continue
        out.append(
            InterfaceSummary(
                section=sec["number"],
                title=sec["title"],
                method=first_non_empty(subs["调用方法"]),
                uri=uri,
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
    print(f"已提取 {len(interfaces)} 个 PoDManager 接口 -> {out}")


if __name__ == "__main__":
    main()
