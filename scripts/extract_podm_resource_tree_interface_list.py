#!/usr/bin/env python3
"""Extract Redfish resource-tree interfaces from the PoDManager resource table."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _defaults import DATA_DIR, OUTPUT_DIR, PODM_DOCX, PODM_DOCX_NAME  # noqa: E402
from _docx_utils import read_source  # noqa: E402
from _interface_list import InterfaceSummary, write_interface_list_yaml  # noqa: E402

DEFAULT_INPUT = PODM_DOCX
DEFAULT_OUTPUT = OUTPUT_DIR / "podm.resource-tree.interface-list.yaml"
METHODS = {"GET", "POST", "PATCH", "DELETE", "PUT"}
DATE_RE = re.compile(r"^\d{8}$")


def clean(value: str) -> str:
    return value.replace("\xa0", " ").strip()


def resource_tree_lines(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if "Redfish接口资源树" in line or "Redfish资源树" in line:
            start = index
            break
    if start is None:
        return lines

    selected: list[str] = []
    for index, line in enumerate(lines[start:], start=start):
        stripped = clean(line)
        if index > start and re.match(r"^\d+\s+\S", stripped):
            break
        selected.append(line)
    return selected


def normalize_uri_text(value: str) -> str:
    uri = clean(value).replace(" ", "")
    if uri.lower().startswith("redfish/"):
        uri = "/" + uri
    return uri


def split_methods(value: str) -> list[str]:
    methods: list[str] = []
    for part in re.split(r"[/,，、\s]+", value):
        method = clean(part).upper()
        if method in METHODS:
            methods.append(method)
    return methods


def is_resource_group(line: str) -> bool:
    if "\t" in line:
        return False
    stripped = clean(line)
    if not stripped or stripped.startswith("表") or stripped.startswith("（"):
        return False
    return stripped.endswith("资源") or stripped in {"公共固定资源"}


def row_cells(line: str) -> tuple[str, str] | None:
    if "\t" not in line:
        return None
    cells = [clean(cell) for cell in line.split("\t")]
    if len(cells) < 2:
        return None
    url, operations = cells[0], cells[1]
    if url in {"URL", "接口", "资源"} or operations == "允许操作":
        return None
    return url, operations


def extract(text: str) -> list[InterfaceSummary]:
    current_group = ""
    inherited_methods: list[str] = []
    interfaces: list[InterfaceSummary] = []
    for line in resource_tree_lines(text):
        stripped = clean(line)
        if not stripped:
            continue
        if is_resource_group(stripped):
            current_group = stripped
            continue

        cells = row_cells(line)
        if cells is None:
            continue
        raw_uri, raw_methods = cells
        uri = normalize_uri_text(raw_uri)
        if not uri.startswith("/redfish"):
            continue
        methods = split_methods(raw_methods)
        if methods:
            inherited_methods = methods
        elif clean(raw_methods) == "":
            methods = inherited_methods or [""]
        for method in methods:
            interfaces.append(
                InterfaceSummary(
                    section=current_group,
                    title=uri,
                    method=method,
                    uri=uri,
                )
            )
    return interfaces


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        first = argv[1]
        if first in {"-h", "--help"}:
            print(
                "usage: extract_podm_resource_tree_interface_list.py [YYYYMMDD | input.docx input.yaml]\n\n"
                "从 PoDManager Redfish 资源树表提取接口清单。传入 YYYYMMDD 时读取 data/<date>/"
                " 下的默认 PoDManager 文档，并写入 output/<date>/podm.resource-tree.interface-list.yaml。"
            )
            sys.exit(0)
        if DATE_RE.match(first):
            inp = DATA_DIR / first / PODM_DOCX_NAME
            out = OUTPUT_DIR / first / "podm.resource-tree.interface-list.yaml"
            if len(argv) > 2:
                out = Path(argv[2])
            return inp, out
        inp = Path(first)
        out = Path(argv[2]) if len(argv) > 2 else inp.with_suffix(".resource-tree.interface-list.yaml")
        return inp, out
    return DEFAULT_INPUT, DEFAULT_OUTPUT


def main(argv: list[str] | None = None) -> None:
    args = sys.argv if argv is None else ["extract_podm_resource_tree_interface_list.py", *argv]
    inp, out = _resolve_io(args)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    interfaces = extract(read_source(inp))
    write_interface_list_yaml(interfaces, out)
    print(f"已提取 {len(interfaces)} 个资源树接口 -> {out}")


if __name__ == "__main__":
    main()
