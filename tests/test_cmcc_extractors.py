from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_cmcc import extract as extract_cmcc_params  # noqa: E402
from extract_cmcc_interface_list import extract as extract_cmcc_list  # noqa: E402


class CmccExtractorsTest(unittest.TestCase):
    def test_extracts_uri_list_from_cmcc_command_format(self) -> None:
        text = "\n".join(
            [
                "6.1.2.1 查询服务器资产",
                "命令功能：",
                "查询服务器资产编码",
                "命令格式：",
                "    请求方法：Get",
                "    URL：https://device_ip/redfish/v1/Systems/system_id",
                "    请求头：X-Auth-Token: auth_value",
                "请求消息体：无",
                "参数说明：",
                "表 14 查询指定系统资源参数说明",
                "参数\t参数说明\t取值\tIT-M\tCT-M",
                "system_id\t系统资源的ID\t1\tM\tM",
                "6.1.9.3 查询管理资源信息",
                "命令格式",
                "操作类型：GET",
                "URL:https://device_ip/redfish/v1/Managers/manager_id",
                "请求头：",
                "X-Auth-Token: auth_value",
            ]
        )

        interfaces = extract_cmcc_list(text)

        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].section, "6.1.2.1")
        self.assertEqual(interfaces[0].title, "查询服务器资产")
        self.assertEqual(interfaces[0].method, "GET")
        self.assertEqual(
            interfaces[0].uri,
            "https://device_ip/redfish/v1/Systems/system_id",
        )
        self.assertEqual(interfaces[1].uri, "https://device_ip/redfish/v1/Managers/manager_id")

    def test_extracts_cmcc_request_and_response_params(self) -> None:
        text = "\n".join(
            [
                "6.1.2.2 设置服务器资产相关信息",
                "命令格式：",
                "操作类型：PATCH",
                "URL：https://device_ip/redfish/v1/Systems/system_id",
                "请求头：",
                "X-Auth-Token: auth_value",
                "Content-Type: header_type",
                "If-Match: ifmatch_value",
                "请求消息体：",
                "{",
                '"AssetTag": tag,',
                '"HostName": name,',
                "“Oem”：{“Public”：{“ConfigurationModel”：model,",
                '"LeakStrategy": power_control',
                "}",
                "参数说明：",
                "表 16 修改指定系统资源属性参数说明",
                "参数\t参数说明\t取值\tIT-M\tCT-M",
                "device_ip\t登录设备的IP地址\tIPv4或IPv6地址\tM\tM",
                "system_id\t系统资源的ID\t1\tM\tM",
                "auth_value\t请求消息的鉴权参数\t会话获得\tM\tM",
                "header_type\t请求消息的格式\tapplication/json\tM\tM",
                "ifmatch_value\t请求消息的匹配参数\tETag\tM\tM",
                "tag\t自定义的资产标签\t字符串\tM\tM",
                "name\t自定义的主机名称\t字符串\tM\tM",
                "表 16 修改指定系统资源属性参数说明（续）",
                "参数\t参数说明\t取值\tIT-M\tCT-M",
                "model\t自定义的典配模型\t202001C1\tM\t",
                "power_control\t液冷服务器漏液后电源控制策略\tManualPowerOff\t\t",
                "输出说明：",
                "表 17 指定系统资源信息",
                "字段\t类型\t说明\tIT-M\tCT-M",
                "AssetTag\t字符串\t指定系统资源的资产编码\tM\tM",
                "HostName\t字符串\t指定系统资源的主机名称\tM\tM",
                "表 17 指定系统资源信息（续）",
                "字段\t类型\t说明\tIT-M\tCT-M",
                "ConfigurationModel\t字符串\t年份+批次+典配型号\tM\t",
            ]
        )

        interfaces = extract_cmcc_params(text)

        self.assertEqual(len(interfaces), 1)
        iface = interfaces[0]
        self.assertEqual(iface.method, "PATCH")
        self.assertEqual(iface.params.path, ["system_id"])
        self.assertEqual(iface.params.header, ["auth_value", "header_type", "ifmatch_value"])
        self.assertEqual(iface.params.body, ["tag", "name", "model", "power_control"])
        self.assertEqual(iface.params.query, [])
        self.assertEqual(
            iface.params.response,
            ["AssetTag", "HostName", "ConfigurationModel"],
        )

    def test_extracts_query_and_response_fields_from_late_parameter_section(self) -> None:
        text = "\n".join(
            [
                "6.1.3.1.3 查询指定处理器资源信息",
                "命令格式",
                "操作类型：GET",
                "URL：https://device_ip/redfish/v1/Systems/system_id/Processors/processor _id",
                "请求头：",
                "X-Auth-Token: auth_value",
                "请求消息体：无",
                "参数说明",
                "表 26 查询指定处理器资源信息参数说明",
                "参数\t参数说明\t取值",
                "system_id\t系统资源的ID\t1",
                "processor _id\t处理器资源的ID\t可从处理器集合资源中获得",
                "auth_value\t执行该GET请求时用于鉴权\t会话获得",
                "使用实例",
                "响应样例：",
                "{",
                '"ProcessorType": "CPU"',
                "}",
                "参数说明：",
                "表 28 查询处理器集合资源信息参数说明",
                "字段\t类型\t说明\tIT-M\tCT-M",
                "ProcessorType\t字符串\t指定处理器资源的类型\tM\tM",
                "TotalCores\t数字\t指定处理器资源的总核数\tM\tM",
                "6.1.3.1.4 查询所有处理器资源信息",
                "命令格式：",
                "操作类型：GET",
                "URL：https://device_ip/redfish/v1/Systems/system_id/Processors?$expand=.",
                "请求头：",
                "X-Auth-Token: auth_value",
            ]
        )

        interfaces = extract_cmcc_params(text)

        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].params.path, ["system_id", "processor_id"])
        self.assertEqual(interfaces[0].params.header, ["auth_value"])
        self.assertEqual(interfaces[0].params.response, ["ProcessorType", "TotalCores"])
        self.assertEqual(interfaces[1].params.path, ["system_id"])
        self.assertEqual(interfaces[1].params.query, ["$expand"])


if __name__ == "__main__":
    unittest.main()
