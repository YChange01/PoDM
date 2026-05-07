from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _interface_list import format_interface_list_yaml  # noqa: E402
from extract_bmc_interface_list import extract as extract_bmc  # noqa: E402
from extract_podm_interface_list import extract as extract_podm  # noqa: E402


class InterfaceListTest(unittest.TestCase):
    def test_podm_interface_list_yaml(self) -> None:
        text = "\n".join(
            [
                "4.2.25 导出日志信息",
                "调用方法",
                "POST",
                "URI",
                "/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}",
            ]
        )

        content = format_interface_list_yaml(extract_podm(text))

        self.assertIn("index: 1", content)
        self.assertIn("section: 4.2.25", content)
        self.assertIn("title: 导出日志信息", content)
        self.assertIn("method: POST", content)
        self.assertIn("/redfish/v1/Managers/{manager_id}/LogServices", content)
        self.assertNotIn("params:", content)

    def test_bmc_interface_list_yaml(self) -> None:
        text = "\n".join(
            [
                "3.19.3 基于SPDM协议获取组件签名测量值",
                "命令格式",
                "操作类型：POST",
                "URL：https://device_ip/redfish/v1/ComponentIntegrity/"
                "component_integrity_id/Actions/"
                "ComponentIntegrity.SPDMGetSignedMeasurements",
            ]
        )

        content = format_interface_list_yaml(extract_bmc(text))

        self.assertIn("index: 1", content)
        self.assertIn("section: 3.19.3", content)
        self.assertIn("title: 基于SPDM协议获取组件签名测量值", content)
        self.assertIn("method: POST", content)
        self.assertIn(
            "https://device_ip/redfish/v1/ComponentIntegrity/"
            "component_integrity_id/Actions/"
            "ComponentIntegrity.SPDMGetSignedMeasurements",
            content,
        )
        self.assertNotIn("params:", content)


if __name__ == "__main__":
    unittest.main()
