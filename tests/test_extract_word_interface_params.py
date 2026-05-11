from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_word_interface_params import (  # noqa: E402
    extract_interfaces_from_text,
    load_common_sections,
)


class ExtractWordInterfaceParamsTest(unittest.TestCase):
    def test_extracts_podm_interface_params_and_types(self) -> None:
        text = "\n".join(
            [
                "4.2.25 导出日志信息",
                "调用方法",
                "POST",
                "URI",
                "/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}",
                "请求参数",
                "Path参数列表",
                "参数名称\t必选\t类型\t参数说明",
                "manager_id\t是\tstring\t管理资源ID",
                "logservices_id\t是\tstring\t日志服务ID",
                "Header参数列表",
                "参数名称\t必选\t类型\t参数说明",
                "X-Auth-Token\t是\tstring\t认证令牌",
                "Query参数列表",
                "参数名称\t必选\t类型\t参数说明",
                "$top\t否\tinteger\t返回数量",
                "Body参数列表",
                "参数名称\t必选\t类型\t参数说明",
                "Type\t是\tstring\t日志类型",
                "响应参数",
                "Response参数列表",
                "参数名称\t类型\t参数说明",
                "@odata.context\tstring\tOData描述信息",
                "Members\tarray\t成员列表",
            ]
        )

        interfaces = extract_interfaces_from_text(text, "podm")

        self.assertEqual(len(interfaces), 1)
        iface = interfaces[0]
        self.assertEqual(iface.method, "POST")
        self.assertEqual(iface.params["path"][0].name, "manager_id")
        self.assertEqual(iface.params["path"][0].type, "string")
        self.assertEqual(iface.params["header"][0].name, "X-Auth-Token")
        self.assertEqual(iface.params["query"][0].name, "$top")
        self.assertEqual(iface.params["query"][0].type, "integer")
        self.assertEqual(iface.params["body"][0].name, "Type")
        self.assertEqual(iface.params["response"][1].name, "Members")
        self.assertEqual(iface.params["response"][1].type, "array")

    def test_extracts_bmc_interface_params_and_types(self) -> None:
        text = "\n".join(
            [
                "3.2.6 一键收集",
                "命令格式",
                "操作类型：POST",
                "URL：https://device_ip/redfish/v1/Managers/manager_id/Actions/Oem/Huawei/Public/Manager.Dump?kind=dump_kind",
                "请求头：",
                "X-Auth-Token: token",
                "请求消息体：",
                '{"Type":"All"}',
                "参数说明",
                "参数\t类型\t说明\t取值",
                "manager_id\tstring\t管理资源ID\t-",
                "X-Auth-Token\tstring\t认证令牌\t-",
                "Type\tstring\t收集类型\tAll",
                "dump_kind\tinteger\t收集种类\t-",
                "输出说明",
                "字段\t类型\t说明",
                "Id\tstring\t任务ID",
                "Messages\t数组\t消息列表",
                "状态\t说明",
                "Successful\t成功",
            ]
        )

        interfaces = extract_interfaces_from_text(text, "bmc")

        self.assertEqual(len(interfaces), 1)
        params = interfaces[0].params
        self.assertEqual(params["path"][0].name, "manager_id")
        self.assertEqual(params["path"][0].type, "string")
        self.assertEqual(params["header"][0].name, "X-Auth-Token")
        self.assertEqual(params["body"][0].name, "Type")
        self.assertEqual(params["query"][0].name, "dump_kind")
        self.assertEqual(params["query"][0].type, "integer")
        self.assertEqual([record.name for record in params["response"]], ["Id", "Messages"])
        self.assertEqual(params["response"][1].type, "数组")

    def test_load_common_sections_from_match_workbook(self) -> None:
        try:
            from openpyxl import Workbook
        except ImportError:
            self.skipTest("openpyxl not installed")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "match.xlsx"
            wb = Workbook()
            ws = wb.active
            ws.title = "共有接口"
            ws.append(["bmc_section", "podm_section"])
            ws.append(["3.1.1", "4.1.1"])
            ws.append(["3.1.2", "4.1.2"])
            wb.save(path)

            self.assertEqual(load_common_sections(path, "bmc", "共有接口"), {"3.1.1", "3.1.2"})
            self.assertEqual(load_common_sections(path, "podm", "共有接口"), {"4.1.1", "4.1.2"})


if __name__ == "__main__":
    unittest.main()
