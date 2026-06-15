#!/usr/bin/env python3
"""Extract CMCC Redfish interface list as index/section/title/method/uri YAML."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cmcc_docx_utils import read_source  # noqa: E402
from _interface_list import InterfaceSummary, write_interface_list_yaml  # noqa: E402
from extract_cmcc import DEFAULT_INPUT, extract as extract_cmcc_interfaces  # noqa: E402
from extract_cmcc import extract_from_path as extract_cmcc_interfaces_from_path  # noqa: E402


DEFAULT_OUTPUT = Path("output/20260610/cmcc.interface-list.yaml")


def extract(text: str) -> list[InterfaceSummary]:
    return [
        InterfaceSummary(
            section=item.section,
            title=item.title,
            method=item.method,
            uri=item.uri,
        )
        for item in extract_cmcc_interfaces(text)
    ]


def resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if argv:
        input_path = Path(argv[0])
        output_path = Path(argv[1]) if len(argv) > 1 else DEFAULT_OUTPUT
        return input_path, output_path
    return DEFAULT_INPUT, DEFAULT_OUTPUT


def main() -> None:
    input_path, output_path = resolve_io(sys.argv[1:])
    if not input_path.exists():
        raise SystemExit(f"输入文件不存在: {input_path}")

    if input_path.suffix.lower() == ".docx":
        interfaces = [
            InterfaceSummary(
                section=item.section,
                title=item.title,
                method=item.method,
                uri=item.uri,
            )
            for item in extract_cmcc_interfaces_from_path(input_path)
        ]
    else:
        interfaces = extract(read_source(input_path))
    write_interface_list_yaml(interfaces, output_path)
    print(f"已提取 {len(interfaces)} 个 CMCC 接口 -> {output_path}")


if __name__ == "__main__":
    main()
