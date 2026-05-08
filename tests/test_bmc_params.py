from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from extract_bmc import extract_response_fields  # noqa: E402


class BmcParamsTest(unittest.TestCase):
    def test_output_description_skips_enum_tables_and_prose(self) -> None:
        lines = [
            "表3-211 查询SP的配置结果资源的信息",
            "字段\t类型\t说明",
            "@odata.context\t字符串\t配置结果资源模型的OData描述信息",
            "Status\t字符串\t配置状态",
            "OSInstall\t对象\t基础部署的结果",
            "Diagnose\t对象，诊断结果",
            "RebootDelayMinutes\t整数\t延迟重启时间，下发诊断任务设置延迟重启时间后显示。",
            "说明",
            "说明：",
            "SP 1.21.0及之后版本支持。",
            "Detail\t数组\t诊断结果详细信息，详情见CPU、内存、硬盘详细信息表",
            "Status\t字符串\t节点任务状态",
            "见下表3-212",
            "表3-212 配置结果状态",
            "状态\t说明",
            "successful\t任务成功",
            "Successful\t诊断成功",
            "Diagnosing\t正在诊断",
            "表3-214 CPU详细信息",
            "字段\t类型\t说明",
            "Name\t字符串\tCPU名称",
            "CPUID\t字符串\tCPU编号",
            "DiagnoseResult\t字符串\t诊断结果",
            "Successful：成功",
            "Failed：失败",
            "表3-221 TaskState任务状态说明",
            "任务状态\t说明",
            "Pending\t等待中",
            "Running\t执行中",
        ]

        fields = extract_response_fields(lines)

        self.assertIn("@odata.context", fields)
        self.assertIn("RebootDelayMinutes", fields)
        self.assertIn("Diagnose", fields)
        self.assertIn("Name", fields)
        self.assertIn("CPUID", fields)
        self.assertNotIn("successful", fields)
        self.assertNotIn("Successful", fields)
        self.assertNotIn("Diagnosing", fields)
        self.assertNotIn("Pending", fields)
        self.assertNotIn("Running", fields)
        self.assertNotIn("CPU详细信息", fields)
        self.assertNotIn("TaskState任务状态说明", fields)


if __name__ == "__main__":
    unittest.main()
