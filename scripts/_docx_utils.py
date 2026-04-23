"""共享 .docx 读取工具。

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
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_TEXT_NUM_PREFIX = re.compile(r"^(\d+(?:\.\d+)*)\s+(.*)$")


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
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    body = tree.getroot().find(f"{W}body")
    if body is None:
        return ""

    out: list[str] = []
    counters = [0] * 9  # 支持到 Heading9

    for child in body:
        tag = child.tag
        if tag == f"{W}p":
            style = _pstyle_val(child)
            if _is_toc(style):
                continue  # 跳过目录段落
            text = _para_text(child)
            level = _heading_level(style)

            if level is None:
                out.append(text)
                continue

            stripped = text.strip()
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
