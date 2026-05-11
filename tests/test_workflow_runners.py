from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_common_word_interface_params import write_param_compare_input  # noqa: E402
from extract_interface_lists import main as extract_interface_lists_main  # noqa: E402


def write_docx_lines(path: Path, lines: list[str]) -> None:
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    paragraphs = [
        f'<w:p><w:r><w:t xml:space="preserve">{line}</w:t></w:r></w:p>'
        for line in lines
    ]
    document = (
        f'<w:document xmlns:w="{ns}"><w:body>'
        + "".join(paragraphs)
        + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class WorkflowRunnersTest(unittest.TestCase):
    def test_extract_interface_lists_writes_copy_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            podm = root / "podm.docx"
            bmc = root / "bmc.docx"
            out_dir = root / "output"

            write_docx_lines(
                podm,
                [
                    "4.1.1 查询Redfish版本信息",
                    "调用方法",
                    "GET",
                    "URI",
                    "/redfish",
                ],
            )
            write_docx_lines(
                bmc,
                [
                    "3.1.1 查询Redfish版本信息",
                    "命令格式",
                    "操作类型：GET",
                    "URL：https://device_ip/redfish",
                ],
            )

            extract_interface_lists_main(
                [
                    "20260511",
                    "--podm-doc",
                    str(podm),
                    "--bmc-doc",
                    str(bmc),
                    "--out-dir",
                    str(out_dir),
                ]
            )

            self.assertTrue((out_dir / "podm.interface-list.yaml").exists())
            self.assertTrue((out_dir / "bmc.interface-list.yaml").exists())
            copy_input = out_dir / "analysis" / "interface_match_llm_input.md"
            self.assertTrue(copy_input.exists())
            content = copy_input.read_text(encoding="utf-8")
            self.assertIn("BMC interface-list.yaml", content)
            self.assertIn("PoDManager interface-list.yaml", content)

    def test_write_param_compare_input_embeds_pairing_and_params(self) -> None:
        try:
            from openpyxl import Workbook
        except ImportError:
            self.skipTest("openpyxl not installed")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workbook = root / "interface_match_llm_summary.xlsx"
            bmc_params = root / "bmc.yaml"
            podm_params = root / "podm.yaml"
            output = root / "compare.md"

            wb = Workbook()
            ws = wb.active
            ws.title = "共有接口"
            ws.append(["bmc_section", "bmc_title", "podm_section", "podm_title"])
            ws.append(["3.1.1", "查询Redfish版本信息", "4.1.1", "查询Redfish版本信息"])
            wb.save(workbook)

            bmc_params.write_text("interfaces:\n- section: 3.1.1\n", encoding="utf-8")
            podm_params.write_text("interfaces:\n- section: 4.1.1\n", encoding="utf-8")

            write_param_compare_input(workbook, bmc_params, podm_params, output)

            content = output.read_text(encoding="utf-8")
            self.assertIn("共有接口配对表", content)
            self.assertIn("3.1.1", content)
            self.assertIn("BMC common interface params", content)
            self.assertIn("PoDManager common interface params", content)


if __name__ == "__main__":
    unittest.main()
