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
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402

# X.Y 或更深，后面紧跟一段可读标题（不以 /{ 空格 开头，且不含 / { }）
HEADING_RE = re.compile(r"^(\d+(?:\.\d+)+)[\s\t]+([^\s/{][^/{}]{0,80})$")
# 目录页页码防御：标题末尾跟着 1-4 位纯数字（前一个字符必须是非数字）
_TRAILING_PAGENO = re.compile(r"(\d{1,4})$")


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


# ---------- 标题识别 ----------

def _strip_trailing_pageno(title: str) -> str:
    """防御：若 title 末尾粘着 1-4 位页码（前一个字符非数字），剥掉。"""
    m = _TRAILING_PAGENO.search(title)
    if m and m.start() > 0 and not title[m.start() - 1].isdigit():
        return title[: m.start()]
    return title


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
            number = match.group(1)
            title = _strip_trailing_pageno(match.group(2).strip().rstrip(" 　：:"))
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
    """在 section 内容里找 marker，返回其后的第一条非空行。

    兼容两种写法：
      - PoDManager: marker 独占一行，value 在下一非空行
      - BMC:        "marker：value" / "marker:value" 同一行
    """
    for i, line in enumerate(lines):
        s = line.strip()
        if s == marker:
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    return lines[j].strip()
            return ""
        for sep in ("：", ":"):
            if s.startswith(marker + sep):
                return s[len(marker) + len(sep):].strip()
    return ""


def extract(text: str) -> list[Heading]:
    sections = _split_sections(text)
    out: list[Heading] = []
    for sec in sections:
        # PoDManager 用 "URI" / "调用方法"；BMC 用 "URL" / "操作类型"。
        # 两套都试，谁先命中算谁。
        uri = _find_following(sec.lines, "URI") or _find_following(sec.lines, "URL")
        method = _find_following(sec.lines, "调用方法") or _find_following(sec.lines, "操作类型")
        out.append(Heading(number=sec.number, title=sec.title, method=method, uri=uri))
    return out


# ---------- 输出格式 ----------

def dedup_prefer_uri(headings: list[Heading]) -> list[Heading]:
    """按 (number, title) 去重：带 URI 的优先；否则保留较后出现的一条。

    较后出现的通常更靠近正文（mini-outline 在前、正文在后），保留它可以让
    4.1、4.1.1、4.1.2… 在输出里呈现正确的阅读顺序。
    """
    best: dict[tuple[str, str], int] = {}
    for i, h in enumerate(headings):
        key = (h.number, h.title)
        prev = best.get(key)
        if prev is None:
            best[key] = i
            continue
        prev_has_uri = bool(headings[prev].uri)
        cur_has_uri = bool(h.uri)
        if cur_has_uri and not prev_has_uri:
            best[key] = i
        elif cur_has_uri == prev_has_uri:
            best[key] = i
    keep = set(best.values())
    return [h for i, h in enumerate(headings) if i in keep]


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
    raw = extract(text)
    headings = dedup_prefer_uri(raw)
    out.write_text(format_tree(headings), encoding="utf-8")
    dropped = len(raw) - len(headings)
    with_uri = sum(1 for h in headings if h.uri)
    dup_note = f"，去重 {dropped} 条" if dropped else ""
    print(
        f"已提取 {len(headings)} 个标题"
        f"（其中 {with_uri} 个接口小节带 URI{dup_note}）-> {out}"
    )


if __name__ == "__main__":
    main()
