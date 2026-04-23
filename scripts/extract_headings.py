#!/usr/bin/env python3
"""
从 Word(.docx) 或纯文本(.txt) 接口文档里提取各级标题，
并在每个接口小节下方附带 URI（若有），存成缩进式 txt。

用法：
    python3 extract_headings.py                      # 使用默认输入
    python3 extract_headings.py <输入文件> [输出文件]

    默认输入：<仓库根>/data/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx
    默认输出：<仓库根>/output/<输入文件名>.headings.txt
              （当显式传入输入但未传输出时）输出写到与输入同名的 .headings.txt

依赖：仅 Python 3 标准库。
"""
from __future__ import annotations

import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# X.Y 或更深，后面紧跟一段可读标题（不以 /{ 空格 开头，且不含 / { }）
HEADING_RE = re.compile(r"^(\d+(?:\.\d+)+)[\s\t]+([^\s/{][^/{}]{0,80})$")


@dataclass(frozen=True)
class Heading:
    number: str
    title: str
    method: str = ""
    uri: str = ""


@dataclass
class _Section:
    number: str
    title: str
    lines: list[str] = field(default_factory=list)


# ---------- 输入读取 ----------

def read_docx(path: Path) -> str:
    """解析 .docx：按文档顺序抽取段落和表格（表格以制表符分隔）。"""
    with zipfile.ZipFile(path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    body = tree.getroot().find(f"{W}body")
    out: list[str] = []
    for child in body:
        tag = child.tag
        if tag == f"{W}p":
            texts = [t.text for t in child.iter(f"{W}t") if t.text]
            out.append("".join(texts))
        elif tag == f"{W}tbl":
            for row in child.iter(f"{W}tr"):
                cells: list[str] = []
                for cell in row.iter(f"{W}tc"):
                    ctext = "".join(t.text for t in cell.iter(f"{W}t") if t.text)
                    cells.append(ctext)
                out.append("\t".join(cells))
    return "\n".join(out)


def read_source(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        text = read_docx(path)
    else:
        text = path.read_text(encoding="utf-8-sig")
    return text.replace("　", " ").replace("\xa0", " ")


# ---------- 标题识别 ----------

def _accept_title(title: str) -> bool:
    if not title:
        return False
    if len(title) > 40 and re.search(r"[：:。]", title):
        return False
    if title.startswith(('"', "'", "HTTP", "http")):
        return False
    return True


def _split_sections(text: str) -> list[_Section]:
    """按 X.Y... 标题切分整个文档。"""
    sections: list[_Section] = []
    current: _Section | None = None
    for line in text.splitlines():
        stripped = line.strip()
        match = HEADING_RE.match(stripped)
        if match:
            number, title = match.group(1), match.group(2).strip().rstrip(" 　：:")
            if not _accept_title(title):
                if current is not None:
                    current.lines.append(line)
                continue
            if current is not None:
                sections.append(current)
            current = _Section(number=number, title=title)
            continue
        if current is not None:
            current.lines.append(line)
    if current is not None:
        sections.append(current)
    return sections


def _find_following(lines: list[str], marker: str) -> str:
    """在 section 内容里找 marker 行，返回其后的第一条非空行。"""
    for i, line in enumerate(lines):
        if line.strip() == marker:
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    return lines[j].strip()
            return ""
    return ""


def extract(text: str) -> list[Heading]:
    sections = _split_sections(text)
    out: list[Heading] = []
    for sec in sections:
        uri = _find_following(sec.lines, "URI")
        method = _find_following(sec.lines, "调用方法")
        out.append(Heading(number=sec.number, title=sec.title, method=method, uri=uri))
    return out


# ---------- 输出格式 ----------

def format_tree(headings: list[Heading]) -> str:
    lines: list[str] = []
    for h in headings:
        depth = h.number.count(".")
        indent = "  " * depth
        lines.append(f"{indent}{h.number} {h.title}")
        if h.uri:
            tag = f"[{h.method}] " if h.method else ""
            lines.append(f"{indent}    {tag}{h.uri}")
    return "\n".join(lines) + "\n"


# ---------- 入口 ----------

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        inp = Path(argv[1])
        out = (
            Path(argv[2])
            if len(argv) > 2
            else inp.with_suffix(".headings.txt")
        )
    else:
        inp = DEFAULT_INPUT
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = DEFAULT_OUTPUT_DIR / f"{inp.stem}.headings.txt"
    return inp, out


def main() -> None:
    inp, out = _resolve_io(sys.argv)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    text = read_source(inp)
    headings = extract(text)
    out.write_text(format_tree(headings), encoding="utf-8")
    with_uri = sum(1 for h in headings if h.uri)
    print(f"已提取 {len(headings)} 个标题（其中 {with_uri} 个接口小节带 URI）-> {out}")


if __name__ == "__main__":
    main()
