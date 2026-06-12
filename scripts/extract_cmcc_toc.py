#!/usr/bin/env python3
"""Extract CMCC document headings into a standalone table of contents."""
from __future__ import annotations

import sys
import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cmcc_docx_utils import preferred_copy_pasted_text, read_source  # noqa: E402
from _doc_structure import _strip_trailing_pageno  # noqa: E402
from _yaml_io import dump_yaml  # noqa: E402
from extract_cmcc import DEFAULT_INPUT, normalize_source_text, parse_heading_title  # noqa: E402


DEFAULT_OUTPUT = Path("output/20260610/cmcc.toc.yaml")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TOC_HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*)[\s\t]+([^\s/{][^{}]{0,100})$")
UNNUMBERED_FRONT_HEADINGS = {"目录", "前言"}


@dataclass
class TocEntry:
    index: int
    section: str
    level: int
    title: str
    line: int


def _w_val(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return elem.get(f"{W}val") or ""


def _normalize_style(style: str) -> str:
    return style.strip().lower().replace(" ", "").replace("-", "").replace("_", "")


def _heading_level_from_name(name: str) -> int | None:
    normalized = _normalize_style(name)
    if not normalized:
        return None
    for level in range(1, 10):
        if normalized in {f"heading{level}", f"标题{level}", f"hdg{level}"}:
            return level
    return None


def _pstyle_val(p_elem: ET.Element) -> str:
    p_style = p_elem.find(f"{W}pPr/{W}pStyle")
    return _w_val(p_style)


def _para_text(p_elem: ET.Element) -> str:
    parts: list[str] = []
    for child in p_elem.iter():
        if child.tag == f"{W}t":
            parts.append(child.text or "")
        elif child.tag == f"{W}tab":
            parts.append("\t")
        elif child.tag == f"{W}br":
            parts.append("\n")
    return "".join(parts)


def _parse_toc_heading(line: str) -> tuple[str, str]:
    stripped = line.strip(" \t▪■●◆◇-")
    match = TOC_HEADING_RE.match(stripped)
    if not match:
        return "", stripped
    return match.group(1), _strip_trailing_pageno(match.group(2).strip())


def _read_style_outline_levels(archive: zipfile.ZipFile) -> dict[str, int]:
    try:
        with archive.open("word/styles.xml") as stream:
            tree = ET.parse(stream)
    except KeyError:
        return {}

    direct_levels: dict[str, int] = {}
    based_on: dict[str, str] = {}

    for style in tree.getroot().findall(f"{W}style"):
        if style.get(f"{W}type") != "paragraph":
            continue
        style_id = style.get(f"{W}styleId") or ""
        if not style_id:
            continue

        parent = _w_val(style.find(f"{W}basedOn"))
        if parent:
            based_on[style_id] = parent

        outline = _w_val(style.find(f"{W}pPr/{W}outlineLvl"))
        if outline:
            try:
                direct_levels[style_id] = int(outline) + 1
                continue
            except ValueError:
                pass

        level = _heading_level_from_name(style_id)
        if level is None:
            level = _heading_level_from_name(_w_val(style.find(f"{W}name")))
        if level is not None:
            direct_levels[style_id] = level

    resolved: dict[str, int | None] = {}

    def resolve(style_id: str, trail: set[str]) -> int | None:
        if style_id in resolved:
            return resolved[style_id]
        if style_id in direct_levels:
            resolved[style_id] = direct_levels[style_id]
            return resolved[style_id]
        parent = based_on.get(style_id)
        if not parent or parent in trail:
            resolved[style_id] = None
            return None
        resolved[style_id] = resolve(parent, trail | {style_id})
        return resolved[style_id]

    style_levels: dict[str, int] = {}
    for style_id in set(direct_levels) | set(based_on):
        level = resolve(style_id, set())
        if level is not None:
            style_levels[style_id] = level
    return style_levels


def _paragraph_outline_level(
    p_elem: ET.Element,
    style_levels: dict[str, int],
) -> int | None:
    outline = _w_val(p_elem.find(f"{W}pPr/{W}outlineLvl"))
    if outline:
        try:
            return int(outline) + 1
        except ValueError:
            pass

    style_id = _pstyle_val(p_elem)
    if not style_id:
        return None
    if style_id in style_levels:
        return style_levels[style_id]
    return _heading_level_from_name(style_id)


def _sync_counters(counters: list[int], section: str) -> None:
    try:
        values = [int(part) for part in section.split(".")]
    except ValueError:
        return
    for index, value in enumerate(values[: len(counters)]):
        counters[index] = value
    for index in range(len(values), len(counters)):
        counters[index] = 0


def _next_section(counters: list[int], level: int) -> str:
    bounded_level = max(1, min(level, len(counters)))
    for index in range(bounded_level - 1):
        if counters[index] == 0:
            counters[index] = 1
    counters[bounded_level - 1] += 1
    for index in range(bounded_level, len(counters)):
        counters[index] = 0
    return ".".join(str(value) for value in counters[:bounded_level])


def _append_entry(
    entries: list[TocEntry],
    seen: set[tuple[str, str]],
    section: str,
    level: int,
    title: str,
    line_number: int,
) -> None:
    if not section or not title:
        return
    key = (section, title)
    if key in seen:
        return
    seen.add(key)
    entries.append(
        TocEntry(
            index=len(entries) + 1,
            section=section,
            level=level,
            title=title,
            line=line_number,
        )
    )


def extract_toc(text: str) -> list[TocEntry]:
    entries: list[TocEntry] = []
    seen: set[tuple[str, str]] = set()
    for line_number, line in enumerate(normalize_source_text(text).splitlines(), start=1):
        section, title = parse_heading_title(line)
        _append_entry(entries, seen, section, section.count(".") + 1, title, line_number)
    return entries


def extract_toc_from_docx(path: Path) -> list[TocEntry]:
    with zipfile.ZipFile(path) as archive:
        style_levels = _read_style_outline_levels(archive)
        with archive.open("word/document.xml") as stream:
            tree = ET.parse(stream)

    body = tree.getroot().find(f"{W}body")
    if body is None:
        return []

    entries: list[TocEntry] = []
    seen: set[tuple[str, str]] = set()
    counters = [0] * 9
    paragraph_number = 0

    for child in body:
        if child.tag != f"{W}p":
            continue
        paragraph_number += 1
        outline_level = _paragraph_outline_level(child, style_levels)
        if outline_level is None:
            continue

        title_text = _para_text(child).strip()
        if not title_text or title_text in UNNUMBERED_FRONT_HEADINGS:
            continue

        section, title = _parse_toc_heading(title_text)
        if section:
            _sync_counters(counters, section)
            level = section.count(".") + 1
        else:
            section = _next_section(counters, outline_level)
            title = title_text
            level = outline_level
        _append_entry(entries, seen, section, level, title, paragraph_number)

    return entries


def extract_toc_from_path(path: Path) -> list[TocEntry]:
    if path.suffix.lower() == ".docx":
        copy_text = preferred_copy_pasted_text(path)
        if copy_text is not None:
            text = copy_text.read_text(encoding="utf-8-sig")
            return extract_toc(text.replace("　", " ").replace("\xa0", " "))
        return extract_toc_from_docx(path)
    return extract_toc(read_source(path))


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

    entries = extract_toc_from_path(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_path = dump_yaml({"toc": [asdict(entry) for entry in entries]}, output_path)
    text_path = write_toc_text(entries, output_path)
    print(f"已提取 {len(entries)} 条 CMCC 目录")
    print(f"  YAML: {yaml_path}")
    print(f"  TXT:  {text_path}")


if __name__ == "__main__":
    main()
