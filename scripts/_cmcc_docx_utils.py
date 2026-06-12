"""CMCC 专用 .docx 读取工具。

CMCC 要求文档里有些接口小节编号只存在于 Word OOXML 的 numbering/style
元数据里，不在段落文本中。这个 reader 会读取这些编号并合成到纯文本里。

这个模块只给 ``extract_cmcc*.py`` 使用，避免影响 PoDManager/BMC 既有提取链路。

与最朴素的"把所有 <w:t> 拼起来"相比，多做两件事：

1. 按段落样式识别**目录段落**并跳过，避免把 ToC 与正文重复读进来
   （TOC 段落的典型表现是末尾粘着页码，例如 "2.1 创建Redfish用户5"）。
2. 对 **Heading N / 标题N** 段落：
   - 若段落文本里已经带 "X.Y.Z" 编号，就以文本为准，并同步计数器；
   - 否则按样式层级用**计数器合成** "X.Y.Z"（处理 Word 自动编号，编号不在文本里的情况）。

表格展开为行，单元格以制表符分隔，供后续 split/regex 消费。
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_TEXT_NUM_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)\s+(.*)$")
_NUM_PLACEHOLDER_RE = re.compile(r"%([1-9])")


@dataclass
class _NumberLevel:
    start: int = 1
    fmt: str = ""
    text: str = ""


@dataclass
class _Numbering:
    num_to_abstract: dict[str, str] = field(default_factory=dict)
    levels: dict[str, dict[int, _NumberLevel]] = field(default_factory=dict)
    overrides: dict[tuple[str, int], int] = field(default_factory=dict)
    style_num_pr: dict[str, tuple[str, int]] = field(default_factory=dict)


# ---------- 样式识别 ----------

def _pstyle_val(p_elem) -> str:
    p_style = p_elem.find(f"{W}pPr/{W}pStyle")
    return (p_style.get(f"{W}val") if p_style is not None else "") or ""


def _normalize_style(style: str) -> str:
    return style.strip().lower().replace(" ", "").replace("-", "").replace("_", "")


def _heading_level(style: str) -> int | None:
    s = _normalize_style(style)
    if not s:
        return None
    for i in range(1, 10):
        if s in {f"heading{i}", f"标题{i}", f"hdg{i}"}:
            return i
    return None


def _is_toc(style: str) -> bool:
    s = _normalize_style(style)
    return s.startswith("toc") or s.startswith("目录")


# ---------- 编号识别 ----------

def _w_val(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return elem.get(f"{W}val") or ""


def _read_numbering(archive: zipfile.ZipFile) -> _Numbering:
    try:
        with archive.open("word/numbering.xml") as f:
            tree = ET.parse(f)
    except KeyError:
        return _Numbering()

    numbering = _Numbering()
    root = tree.getroot()

    for abstract in root.findall(f"{W}abstractNum"):
        abstract_id = abstract.get(f"{W}abstractNumId") or ""
        if not abstract_id:
            continue
        levels: dict[int, _NumberLevel] = {}
        for level in abstract.findall(f"{W}lvl"):
            raw_ilvl = level.get(f"{W}ilvl") or "0"
            try:
                ilvl = int(raw_ilvl)
            except ValueError:
                continue
            raw_start = _w_val(level.find(f"{W}start"))
            try:
                start = int(raw_start) if raw_start else 1
            except ValueError:
                start = 1
            levels[ilvl] = _NumberLevel(
                start=start,
                fmt=_w_val(level.find(f"{W}numFmt")),
                text=_w_val(level.find(f"{W}lvlText")),
            )
        numbering.levels[abstract_id] = levels

    for num in root.findall(f"{W}num"):
        num_id = num.get(f"{W}numId") or ""
        abstract_id = _w_val(num.find(f"{W}abstractNumId"))
        if num_id and abstract_id:
            numbering.num_to_abstract[num_id] = abstract_id
        for override in num.findall(f"{W}lvlOverride"):
            raw_ilvl = override.get(f"{W}ilvl") or "0"
            raw_start = _w_val(override.find(f"{W}startOverride"))
            try:
                ilvl = int(raw_ilvl)
                start = int(raw_start)
            except ValueError:
                continue
            numbering.overrides[(num_id, ilvl)] = start

    return numbering


def _read_style_numbering(archive: zipfile.ZipFile, numbering: _Numbering) -> None:
    try:
        with archive.open("word/styles.xml") as f:
            tree = ET.parse(f)
    except KeyError:
        return

    direct: dict[str, tuple[str, int]] = {}
    based_on: dict[str, str] = {}
    for style in tree.getroot().findall(f"{W}style"):
        style_id = style.get(f"{W}styleId") or ""
        if not style_id:
            continue
        parent = _w_val(style.find(f"{W}basedOn"))
        if parent:
            based_on[style_id] = parent
        num_pr = style.find(f"{W}pPr/{W}numPr")
        if num_pr is None:
            continue
        num_id = _w_val(num_pr.find(f"{W}numId"))
        raw_ilvl = _w_val(num_pr.find(f"{W}ilvl")) or "0"
        if not num_id:
            continue
        try:
            ilvl = int(raw_ilvl)
        except ValueError:
            ilvl = 0
        direct[style_id] = (num_id, ilvl)

    resolved: dict[str, tuple[str, int] | None] = {}

    def resolve(style_id: str, trail: set[str]) -> tuple[str, int] | None:
        if style_id in resolved:
            return resolved[style_id]
        if style_id in direct:
            resolved[style_id] = direct[style_id]
            return resolved[style_id]
        parent = based_on.get(style_id)
        if not parent or parent in trail:
            resolved[style_id] = None
            return None
        resolved[style_id] = resolve(parent, trail | {style_id})
        return resolved[style_id]

    for style_id in set(direct) | set(based_on):
        value = resolve(style_id, set())
        if value is not None:
            numbering.style_num_pr[style_id] = value


def _paragraph_numbering(p_elem: ET.Element, numbering: _Numbering) -> tuple[str, int] | None:
    num_pr = p_elem.find(f"{W}pPr/{W}numPr")
    if num_pr is not None:
        num_id = _w_val(num_pr.find(f"{W}numId"))
        raw_ilvl = _w_val(num_pr.find(f"{W}ilvl")) or "0"
        if num_id:
            try:
                ilvl = int(raw_ilvl)
            except ValueError:
                ilvl = 0
            return num_id, ilvl

    style = _pstyle_val(p_elem)
    if style:
        return numbering.style_num_pr.get(style)
    return None


def _level_start(
    numbering: _Numbering,
    num_id: str,
    abstract_id: str,
    ilvl: int,
) -> int:
    if (num_id, ilvl) in numbering.overrides:
        return numbering.overrides[(num_id, ilvl)]
    level = numbering.levels.get(abstract_id, {}).get(ilvl)
    return level.start if level is not None else 1


def _numbering_prefix(
    p_elem: ET.Element,
    numbering: _Numbering,
    counters: dict[str, list[int]],
) -> str:
    num_pr = _paragraph_numbering(p_elem, numbering)
    if num_pr is None:
        return ""
    num_id, ilvl = num_pr
    abstract_id = numbering.num_to_abstract.get(num_id, "")
    level = numbering.levels.get(abstract_id, {}).get(ilvl)
    if level is None or level.fmt == "bullet" or "%" not in level.text:
        return ""

    values = counters.setdefault(num_id, [0] * 9)
    for i in range(ilvl):
        if values[i] == 0:
            values[i] = _level_start(numbering, num_id, abstract_id, i)
    if values[ilvl] == 0:
        values[ilvl] = _level_start(numbering, num_id, abstract_id, ilvl)
    else:
        values[ilvl] += 1
    for i in range(ilvl + 1, len(values)):
        values[i] = 0

    def replace(match: re.Match[str]) -> str:
        index = int(match.group(1)) - 1
        return str(values[index]) if 0 <= index < len(values) else ""

    return _NUM_PLACEHOLDER_RE.sub(replace, level.text).strip()


# ---------- 文本/表格抽取 ----------

def _para_text(p_elem) -> str:
    return "".join((t.text or "") for t in p_elem.iter(f"{W}t"))


def _table_rows(tbl_elem) -> list[str]:
    rows: list[str] = []
    for row in tbl_elem.iter(f"{W}tr"):
        cells: list[str] = []
        for cell in row.iter(f"{W}tc"):
            cells.append("".join((t.text or "") for t in cell.iter(f"{W}t")))
        rows.append("\t".join(cells))
    return rows


# ---------- 主流程 ----------

def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        numbering = _read_numbering(z)
        _read_style_numbering(z, numbering)
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    body = tree.getroot().find(f"{W}body")
    if body is None:
        return ""

    out: list[str] = []
    counters = [0] * 9  # 支持到 Heading9
    numbering_counters: dict[str, list[int]] = {}

    for child in body:
        tag = child.tag
        if tag == f"{W}p":
            style = _pstyle_val(child)
            if _is_toc(style):
                continue  # 跳过目录段落
            text = _para_text(child)
            stripped = text.strip()
            num_prefix = _numbering_prefix(child, numbering, numbering_counters)
            if num_prefix and stripped and not stripped.startswith(num_prefix):
                out.append(f"{num_prefix} {stripped}")
                continue
            level = _heading_level(style)

            if level is None:
                out.append(text)
                continue

            m = _TEXT_NUM_PREFIX.match(stripped)
            if m:
                # 文本里已带 X.Y.Z — 以它为准同步计数器
                nums = [int(x) for x in m.group(1).split(".")]
                for i, n in enumerate(nums):
                    if i < len(counters):
                        counters[i] = n
                for i in range(len(nums), len(counters)):
                    counters[i] = 0
                out.append(text)
            elif stripped and 1 <= level <= len(counters):
                # 按标题层级递增计数器，合成 X.Y.Z
                counters[level - 1] += 1
                for i in range(level, len(counters)):
                    counters[i] = 0
                num = ".".join(str(c) for c in counters[:level])
                out.append(f"{num} {stripped}")
            else:
                out.append(text)
        elif tag == f"{W}tbl":
            out.extend(_table_rows(child))

    return "\n".join(out)


def read_source(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        text = read_docx(path)
    else:
        text = path.read_text(encoding="utf-8-sig")
    return text.replace("　", " ").replace("\xa0", " ")
