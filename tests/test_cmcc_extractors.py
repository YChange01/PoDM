from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from _cmcc_docx_utils import read_source as read_cmcc_source  # noqa: E402
from _docx_utils import read_source as read_shared_source  # noqa: E402
from extract_cmcc import extract as extract_cmcc_params  # noqa: E402
from extract_cmcc import split_command_blocks  # noqa: E402
from extract_cmcc_interface_list import extract as extract_cmcc_list  # noqa: E402
from extract_cmcc_toc import extract_toc  # noqa: E402


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def write_numbered_cmcc_docx(path: Path) -> None:
    document = f"""
<w:document xmlns:w="{W_NS}">
  <w:body>
    <w:p>
      <w:pPr>
        <w:numPr>
          <w:ilvl w:val="3"/>
          <w:numId w:val="1"/>
        </w:numPr>
      </w:pPr>
      <w:r><w:t>修改BMC管理服务信息</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t>命令功能</w:t></w:r></w:p>
    <w:p><w:r><w:t>修改服务器 BMC 管理服务状态及端口信息。</w:t></w:r></w:p>
    <w:p><w:r><w:t>命令格式</w:t></w:r></w:p>
    <w:p><w:r><w:t>操作类型：PATCH</w:t></w:r></w:p>
    <w:p><w:r><w:t>URL:https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol</w:t></w:r></w:p>
    <w:p><w:r><w:t>请求头：</w:t></w:r></w:p>
    <w:p><w:r><w:t>X-Auth-Token: auth_value</w:t></w:r></w:p>
    <w:p><w:r><w:t>请求消息体：无</w:t></w:r></w:p>
  </w:body>
</w:document>
""".strip()
    numbering = f"""
<w:numbering xmlns:w="{W_NS}">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0"><w:start w:val="6"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1"/></w:lvl>
    <w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2"/></w:lvl>
    <w:lvl w:ilvl="2"><w:start w:val="9"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3"/></w:lvl>
    <w:lvl w:ilvl="3"><w:start w:val="10"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3.%4"/></w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>
""".strip()
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)
        archive.writestr("word/numbering.xml", numbering)


def write_style_numbered_cmcc_docx(path: Path) -> None:
    document = f"""
<w:document xmlns:w="{W_NS}">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="CmccApiHeading"/></w:pPr>
      <w:r><w:t>修改BMC管理服务信息</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t>命令功能</w:t></w:r></w:p>
    <w:p><w:r><w:t>修改服务器 BMC 管理服务状态及端口信息。</w:t></w:r></w:p>
    <w:p><w:r><w:t>命令格式</w:t></w:r></w:p>
    <w:p><w:r><w:t>操作类型：PATCH</w:t></w:r></w:p>
    <w:p><w:r><w:t>URL:https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol</w:t></w:r></w:p>
    <w:p><w:r><w:t>请求头：</w:t></w:r></w:p>
    <w:p><w:r><w:t>X-Auth-Token: auth_value</w:t></w:r></w:p>
    <w:p><w:r><w:t>请求消息体：无</w:t></w:r></w:p>
  </w:body>
</w:document>
""".strip()
    styles = f"""
<w:styles xmlns:w="{W_NS}">
  <w:style w:type="paragraph" w:styleId="CmccApiHeading">
    <w:name w:val="Cmcc API Heading"/>
    <w:pPr>
      <w:numPr>
        <w:ilvl w:val="3"/>
        <w:numId w:val="1"/>
      </w:numPr>
    </w:pPr>
  </w:style>
</w:styles>
""".strip()
    numbering = f"""
<w:numbering xmlns:w="{W_NS}">
  <w:abstractNum w:abstractNumId="0">
    <w:lvl w:ilvl="0"><w:start w:val="6"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1"/></w:lvl>
    <w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2"/></w:lvl>
    <w:lvl w:ilvl="2"><w:start w:val="9"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3"/></w:lvl>
    <w:lvl w:ilvl="3"><w:start w:val="10"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1.%2.%3.%4"/></w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>
""".strip()
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", styles)
        archive.writestr("word/numbering.xml", numbering)


def write_plain_cmcc_docx(path: Path) -> None:
    document = f"""
<w:document xmlns:w="{W_NS}">
  <w:body>
    <w:p><w:r><w:t>修改BMC管理服务信息</w:t></w:r></w:p>
    <w:p><w:r><w:t>命令功能</w:t></w:r></w:p>
    <w:p><w:r><w:t>修改服务器BMC管理服务状态及端口信息。</w:t></w:r></w:p>
    <w:p><w:r><w:t>命令格式</w:t></w:r></w:p>
    <w:p><w:r><w:t>操作类型：PATCH</w:t></w:r></w:p>
    <w:p><w:r><w:t>URL:https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol</w:t></w:r></w:p>
  </w:body>
</w:document>
""".strip()
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document)


class CmccExtractorsTest(unittest.TestCase):
    def test_extracts_cmcc_toc_from_copy_pasted_headings(self) -> None:
        text = "\n".join(
            [
                "Port\t数字\t服务的端口号\tM\tM",
                "6.1.3.7.3\t修改指定电源属性",
                "命令功能",
                "修改服务器指定电源属性。",
                "6.1.3.8 PCIe设备管理要求",
                "该章节的PCIe设备包含人工智能标卡、人工智能模组等PCIe设备",
                "6.1.3.8.1\t查询PCIe设备集合资源信息",
                "6.1.3.8.2 查询指定PCIe设备资源信息45",
            ]
        )

        toc = extract_toc(text)

        self.assertEqual(
            [(item.section, item.level, item.title) for item in toc],
            [
                ("6.1.3.7.3", 5, "修改指定电源属性"),
                ("6.1.3.8", 4, "PCIe设备管理要求"),
                ("6.1.3.8.1", 5, "查询PCIe设备集合资源信息"),
                ("6.1.3.8.2", 5, "查询指定PCIe设备资源信息"),
            ],
        )

    def test_shared_docx_reader_does_not_apply_cmcc_numbering_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cmcc.docx"
            write_style_numbered_cmcc_docx(docx)

            text = read_shared_source(docx)

        self.assertIn("修改BMC管理服务信息", text)
        self.assertNotIn("6.1.9.10 修改BMC管理服务信息", text)

    def test_cmcc_docx_prefers_copy_pasted_sidecar_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cmcc.docx"
            write_plain_cmcc_docx(docx)
            docx.with_suffix(".paste.txt").write_text(
                "\n".join(
                    [
                        "Port\t数字\t服务的端口号\tM\tM",
                        "6.1.9.10 修改BMC管理服务信息",
                        "命令功能",
                        "修改服务器BMC管理服务状态及端口信息。",
                        "命令格式",
                        "操作类型：PATCH",
                        "URL:https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol",
                    ]
                ),
                encoding="utf-8",
            )

            interfaces = extract_cmcc_params(read_cmcc_source(docx))

        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].section, "6.1.9.10")
        self.assertEqual(interfaces[0].title, "修改BMC管理服务信息")

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

    def test_falls_back_to_command_blocks_when_heading_numbers_are_missing(self) -> None:
        text = "\n".join(
            [
                "查询服务器资产",
                "命令功能：",
                "查询服务器资产编码、主机名、制造厂商",
                "命令格式：",
                "请求方法：Get",
                "URL：https://device_ip/redfish/v1/Systems/system_id",
                "请求头：X-Auth-Token: auth_value",
                "请求消息体：无",
                "参数说明：",
                "表 14 查询指定系统资源参数说明",
                "参数\t参数说明\t取值\tIT-M\tCT-M",
                "device_ip\t登录设备的IP地址\tIPv4或IPv6地址\tM\tM",
                "system_id\t系统资源的ID\t1\tM\tM",
                "auth_value\t执行该GET请求时用于鉴权\t会话获得\tM\tM",
                "输出说明：",
                "表 15 指定系统资源信息",
                "字段\t类型\t说明\tIT-M\tCT-M",
                "AssetTag\t字符串\t指定系统资源的资产编码\tM\tM",
                "HostName\t字符串\t指定系统资源的主机名称\tM\tM",
            ]
        )

        interfaces = extract_cmcc_params(text)

        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].section, "")
        self.assertEqual(interfaces[0].title, "查询服务器资产")
        self.assertEqual(interfaces[0].method, "GET")
        self.assertEqual(
            interfaces[0].uri,
            "https://device_ip/redfish/v1/Systems/system_id",
        )
        self.assertEqual(interfaces[0].params.path, ["system_id"])
        self.assertEqual(interfaces[0].params.header, ["auth_value"])
        self.assertEqual(interfaces[0].params.response, ["AssetTag", "HostName"])

    def test_prefers_command_blocks_when_generated_sections_are_too_coarse(self) -> None:
        text = "\n".join(
            [
                "22.1 资产管理接口要求",
                "表 13 资产管理需求规格表",
                "序号\t功能\t功能描述",
                "1\t资产编码设置\t服务器资产编号设置",
                "查询服务器资产",
                "命令功能：",
                "查询服务器资产编码、主机名、制造厂商",
                "命令格式：",
                "请求方法：Get",
                "URL：https://device_ip/redfish/v1/Systems/system_id",
                "请求头：X-Auth-Token: auth_value",
                "请求消息体：无",
                "参数说明：",
                "表 14 查询指定系统资源参数说明",
                "参数\t参数说明\t取值\tIT-M\tCT-M",
                "system_id\t系统资源的ID\t1\tM\tM",
                "auth_value\t执行该GET请求时用于鉴权\t会话获得\tM\tM",
                "设置服务器资产相关信息",
                "命令功能：",
                "修改指定系统资源属性，包括资产编码、主机名称、典配模型。",
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
                '"HostName": name',
                "}",
            ]
        )

        interfaces = extract_cmcc_params(text)

        self.assertEqual(len(interfaces), 2)
        self.assertEqual(interfaces[0].title, "查询服务器资产")
        self.assertEqual(interfaces[0].method, "GET")
        self.assertEqual(
            interfaces[0].uri,
            "https://device_ip/redfish/v1/Systems/system_id",
        )
        self.assertEqual(interfaces[1].title, "设置服务器资产相关信息")
        self.assertEqual(interfaces[1].method, "PATCH")

    def test_command_blocks_keep_tab_separated_copy_pasted_sections(self) -> None:
        text = "\n".join(
            [
                "Port\t数字\t服务的端口号\tM\tM",
                "6.1.3.7.3\t修改指定电源属性",
                "命令功能",
                "修改服务器指定电源属性。",
                "命令格式",
                "操作类型：PATCH",
                "URL：https://device_ip/redfish/v1/Chassis/chassis_id/Power",
                "请求头：",
                "X-Auth-Token: auth_value",
                "Content-Type: header_type",
                "If-Match: ifmatch_value",
                "请求消息体：无",
                "输出说明",
                "字段\t类型\t说明\tIT-M\tCT-M",
                "Mode\t字符串\t指定电源冗余组\tM\t",
                "6.1.3.8 PCIe设备管理要求",
                "该章节的PCIe设备包含人工智能标卡、人工智能模组等PCIe设备",
                "6.1.3.8.1\t查询PCIe设备集合资源信息",
                "命令功能",
                "查询服务器PCIe设备集合资源信息。",
                "命令格式",
                "操作类型：GET",
                "URL：https://device_ip/redfish/v1/Chassis/chassis_id/PCIeDevices",
                "请求头：",
                "X-Auth-Token: auth_value",
                "请求消息体：无",
            ]
        )

        sections = split_command_blocks(text)

        self.assertEqual(sections[0]["number"], "6.1.3.7.3")
        self.assertEqual(sections[0]["title"], "修改指定电源属性")
        self.assertEqual(sections[1]["number"], "6.1.3.8.1")
        self.assertEqual(sections[1]["title"], "查询PCIe设备集合资源信息")

    def test_extracts_section_from_bullet_prefixed_heading(self) -> None:
        text = "\n".join(
            [
                "▪ 6.1.9.10 修改BMC管理服务信息",
                "命令功能",
                "修改服务器 BMC 管理服务状态及端口信息。",
                "命令格式",
                "操作类型：PATCH",
                "URL:https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol",
                "请求头：",
                "X-Auth-Token: auth_value",
                "Content-Type: header_type",
                "If-Match: ifmatch_value",
                "请求消息体：",
                "{",
                '"HTTPS": https_value',
                "}",
                "参数说明",
                "表 151 修改BMC管理服务信息参数说明",
                "参数\t参数说明\t取值",
                "manager_id\t管理资源的ID\t1",
                "auth_value\t鉴权参数\t会话获得",
                "header_type\t请求消息的格式\tapplication/json",
                "ifmatch_value\t请求消息的匹配参数\tETag",
                "https_value\tHTTPS服务开关\ttrue",
            ]
        )

        interfaces = extract_cmcc_params(text)

        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].section, "6.1.9.10")
        self.assertEqual(interfaces[0].title, "修改BMC管理服务信息")
        self.assertEqual(interfaces[0].method, "PATCH")
        self.assertEqual(
            interfaces[0].uri,
            "https://device_ip/redfish/v1/Managers/manager_id/NetworkProtocol",
        )
        self.assertEqual(interfaces[0].params.path, ["manager_id"])
        self.assertEqual(
            interfaces[0].params.header,
            ["auth_value", "header_type", "ifmatch_value"],
        )
        self.assertEqual(interfaces[0].params.body, ["https_value"])

    def test_extracts_section_from_word_numbered_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cmcc.docx"
            write_numbered_cmcc_docx(docx)

            interfaces = extract_cmcc_params(read_cmcc_source(docx))

        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].section, "6.1.9.10")
        self.assertEqual(interfaces[0].title, "修改BMC管理服务信息")

    def test_extracts_section_from_style_numbered_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "cmcc.docx"
            write_style_numbered_cmcc_docx(docx)

            interfaces = extract_cmcc_params(read_cmcc_source(docx))

        self.assertEqual(len(interfaces), 1)
        self.assertEqual(interfaces[0].section, "6.1.9.10")
        self.assertEqual(interfaces[0].title, "修改BMC管理服务信息")


if __name__ == "__main__":
    unittest.main()
