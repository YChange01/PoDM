"""打印 .docx 里所有段落样式的分布 + 每种样式首次出现时的文本样本。

排查 Word 标题/目录/正文样式名称是否为脚本预期的 "Heading N / 标题N / TOCn"。

用法:
    python3 scripts/docx_diag.py                 # 用默认输入
    python3 scripts/docx_diag.py <path.docx>

依赖：仅 Python 3 标准库。
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"


def _style(p_elem) -> str:
    ps = p_elem.find(f"{W}pPr/{W}pStyle")
    return (ps.get(f"{W}val") if ps is not None else "(none)") or "(none)"


def _text(p_elem) -> str:
    return "".join((t.text or "") for t in p_elem.iter(f"{W}t")).strip()


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not path.exists():
        sys.exit(f"输入文件不存在: {path}")

    with zipfile.ZipFile(path) as z:
        with z.open("word/document.xml") as f:
            tree = ET.parse(f)
    body = tree.getroot().find(f"{W}body")
    if body is None:
        sys.exit("文档 body 为空")

    styles: Counter[str] = Counter()
    sample: dict[str, str] = {}
    for child in body:
        if child.tag == f"{W}p":
            s = _style(child)
            styles[s] += 1
            if s not in sample:
                sample[s] = _text(child)[:60]

    print(f"{'style':<30} {'count':>8}  first-text-sample")
    print("-" * 90)
    for style, count in styles.most_common():
        print(f"{style:<30} {count:>8}  {sample.get(style, '')}")


if __name__ == "__main__":
    main()
