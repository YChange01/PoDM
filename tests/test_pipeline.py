from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_pipeline import run_pipeline  # noqa: E402


def write_docx_lines(path: Path, lines: list[str]) -> None:
    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    paragraphs = []
    for line in lines:
        paragraphs.append(
            f'<w:p><w:r><w:t xml:space="preserve">{line}</w:t></w:r></w:p>'
        )
    document = (
        f'<w:document xmlns:w="{ns}"><w:body>'
        + "".join(paragraphs)
        + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", document)


class PipelineTest(unittest.TestCase):
    def test_run_pipeline_outputs_to_date_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data_dir = root / "data" / "20260507"
            data_dir.mkdir(parents=True)
            podm = data_dir / "Atlas PoDManager 1.0.0 Redfish 接口参考.docx"
            bmc = data_dir / "华为服务器 iBMC300 Redfish 接口说明.docx"
            output_root = root / "output"

            write_docx_lines(
                podm,
                [
                    "4.2.25 导出日志信息",
                    "调用方法",
                    "POST",
                    "URI",
                    "/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}",
                    "请求示例",
                    "POST /redfish/v1/Managers/{manager_id}/LogServices/{logservices_id} HTTP/1.1",
                    "X-Auth-Token: token",
                    '{"Type":"All"}',
                    "响应示例",
                    '{"Id":"1"}',
                ],
            )
            write_docx_lines(
                bmc,
                [
                    "3.19.3 基于SPDM协议获取组件签名测量值",
                    "命令格式",
                    "操作类型：POST",
                    "URL：https://device_ip/redfish/v1/ComponentIntegrity/"
                    "component_integrity_id/Actions/"
                    "ComponentIntegrity.SPDMGetSignedMeasurements",
                    "请求头：",
                    "X-Auth-Token: token",
                    "请求消息体：",
                    '{"Nonce":"abc"}',
                    "输出说明",
                    "字段 类型 说明",
                    "Id string 标识",
                ],
            )

            out_dir = run_pipeline("20260507", output_root, podm, bmc)

            self.assertEqual(out_dir, (output_root / "20260507").resolve())
            self.assertTrue((out_dir / f"{podm.stem}.interface-list.yaml").exists())
            self.assertTrue((out_dir / f"{bmc.stem}.interface-list.yaml").exists())
            self.assertTrue((out_dir / f"{podm.stem}.uris.txt").exists())
            self.assertTrue((out_dir / f"{podm.stem}.example.uris.txt").exists())
            self.assertTrue((out_dir / f"{bmc.stem}.bmc.uris.txt").exists())

            podm_params = out_dir / f"{podm.stem}.interfaces.yaml"
            bmc_params = out_dir / f"{bmc.stem}.bmc.interfaces.yaml"
            self.assertTrue(podm_params.exists() or podm_params.with_suffix(".json").exists())
            self.assertTrue(bmc_params.exists() or bmc_params.with_suffix(".json").exists())


if __name__ == "__main__":
    unittest.main()
