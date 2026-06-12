from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from docx_to_text import convert_docx_to_text, write_docx_text  # noqa: E402


NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def paragraph(text: str, style: str | None = None) -> str:
    style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return (
        f"<w:p>{style_xml}"
        f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'
        "</w:p>"
    )


def table(rows: list[list[str]]) -> str:
    row_xml = []
    for row in rows:
        cells = "".join(
            f"<w:tc><w:p><w:r><w:t>{cell}</w:t></w:r></w:p></w:tc>"
            for cell in row
        )
        row_xml.append(f"<w:tr>{cells}</w:tr>")
    return f"<w:tbl>{''.join(row_xml)}</w:tbl>"


def write_docx(path: Path, body_parts: list[str]) -> None:
    document = (
        f'<w:document xmlns:w="{NS}"><w:body>'
        + "".join(body_parts)
        + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class DocxToTextTest(unittest.TestCase):
    def test_converts_docx_to_extraction_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "接口文档.docx"
            write_docx(
                docx,
                [
                    paragraph("4.1 查询接口", "TOC1"),
                    paragraph("接口说明", "Heading1"),
                    paragraph("URI"),
                    paragraph("/redfish/v1"),
                    table(
                        [
                            ["参数名称", "必选", "类型", "参数说明"],
                            ["ManagerId", "是", "string", "管理器ID"],
                        ]
                    ),
                ],
            )

            text = convert_docx_to_text(docx)

        self.assertEqual(
            text,
            "\n".join(
                [
                    "1 接口说明",
                    "URI",
                    "/redfish/v1",
                    "参数名称\t必选\t类型\t参数说明",
                    "ManagerId\t是\tstring\t管理器ID",
                ]
            ),
        )

    def test_write_docx_text_defaults_to_input_stem_txt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docx = root / "接口文档.docx"
            write_docx(docx, [paragraph("URI"), paragraph("/redfish/v1")])

            output = write_docx_text(docx)

            self.assertEqual(output, root / "接口文档.extraction.txt")
            self.assertEqual(output.read_text(encoding="utf-8"), "URI\n/redfish/v1")


if __name__ == "__main__":
    unittest.main()
