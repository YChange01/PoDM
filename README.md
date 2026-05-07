# PoDM 接口文档提取工具

从 Redfish 接口文档（Word `.docx` 或纯文本 `.txt`）中提取接口清单与接口参数，
方便后续做跨版本 / 跨产品（如 BMC vs PoDM）的对比分析。

> 零第三方依赖：仅用 Python 3 标准库（`zipfile` + `xml.etree`）直读 `.docx`，
> 不需要 `pandoc` / `python-docx` / `pip` 安装。
> 若安装了 `PyYAML`，两份 interfaces.yaml 会用 YAML 输出，否则自动回退 JSON。

## 两条独立的参数提取路径

同一份 docx 里，参数在两个地方各出现一次：**参数表** 和 **请求/响应示例代码**。
两个地方**互为校验**——理想情况下应一致，不一致就是文档 bug。所以仓库里有
**两个独立的提取脚本**，字段和输出结构完全对称，便于 diff：

| 路径 | 数据源 | 脚本 |
|---|---|---|
| 表格路径 | "请求参数 / 响应参数" 小节里的参数表 | `scripts/extract_from_tables.py` |
| 示例路径 | "请求示例 / 响应示例" 小节里的 HTTP 报文和 JSON | `scripts/extract_from_examples.py` |

两条路径的实现彼此独立（比如 marker 识别规则不同——示例里有 "请求示例 1 / 响应示例 2"
这种带空格数字后缀的写法；表格没有）。互不共享状态，一边优化不会影响另一边。

## 目录结构

```
PoDM/
├── README.md
├── .gitignore
├── pyproject.toml
├── scripts/
│   ├── _docx_utils.py                # 共享 .docx 读取 (跳 ToC + 合成 X.Y.Z 编号)
│   ├── _defaults.py                  # 默认文档名 / data-output-analysis 路径
│   ├── _interface_list.py            # 接口清单 YAML 输出
│   ├── extract_podm_interface_list.py # PoDM：提取接口清单（不含参数）
│   ├── extract_bmc_interface_list.py  # BMC：提取接口清单（不含参数）
│   ├── extract_from_tables.py        # 路径①：从表格提取 URI + 参数 (同时产出 uris.txt)
│   ├── extract_from_examples.py      # 路径②：从示例代码提取 URI + 参数 (同时产出 uris.txt)
│   ├── extract_bmc.py                # BMC：提取接口 + 参数
│   ├── run_pipeline.py               # 一键跑完整提取流水线
│   ├── check.py                      # 编译 + 单元测试
│   ├── col_enum.py                   # 诊断：按列索引枚举表格某列取值
│   ├── type_enum.py                  # 诊断：枚举参数表"类型"列的取值
│   ├── docx_diag.py                  # 诊断：打印段落样式分布
│   └── section_dump.py               # 诊断：导出指定章节的原文
├── analysis/                         # 一次性对比分析 (BMC vs PoDM)
│   ├── error_cases.md / .docx
│   ├── cross_doc_diff.md / .docx
│   └── why_missing_classification.md
├── data/                             # 原始文档（.docx / .txt），不入库
├── output/                           # 脚本生成的结果，不入库
└── tests/                            # 标准库 unittest 冒烟测试
```

`data/` 与 `output/` 目录只保留空壳（`.gitkeep`），内部文件默认被 `.gitignore` 屏蔽。

## 主工作流

本项目现在按两类任务管理：

1. **提取接口清单**：只输出 `index / section / title / method / uri`，不含参数。
2. **提取接口 + 参数**：输出接口元数据和 `path/header/body/query/response` 参数。

| 脚本 | 作用 | 默认输出 |
|---|---|---|
| `scripts/extract_podm_interface_list.py` | PoDManager：提取接口清单（index/section/title/method/uri，不含参数） | `<PoDM stem>.interface-list.yaml` |
| `scripts/extract_bmc_interface_list.py` | BMC：提取接口清单（index/section/title/method/uri，不含参数） | `<BMC stem>.interface-list.yaml` |
| `scripts/extract_from_tables.py` | **表格路径**：从参数表抽 URI + path/header/body/query/response | `<input>.interfaces.yaml` + `<input>.uris.txt` |
| `scripts/extract_from_examples.py` | **示例路径**：从请求/响应示例代码抽相同字段结构 | `<input>.example.interfaces.yaml` + `<input>.example.uris.txt` |
| `scripts/extract_bmc.py` | BMC：从命令格式 / 输出说明抽 URI + 参数 | `<input>.bmc.interfaces.yaml` + `<input>.bmc.uris.txt` |
| `scripts/run_pipeline.py` | 一键跑两份文档的接口清单和接口+参数提取 | `output/<date>/` |

## 用法

把原始文档放到 `data/<日期>/`，输出落在 `output/<日期>/`。

**一键执行**需要传日期参数。脚本会读取 `data/<日期>/` 下的固定文件名，并输出到
`output/<日期>/`：

```bash
python3 scripts/run_pipeline.py 20260507
```

输入文件应为：

```text
data/20260507/Atlas PoDManager 1.0.0 Redfish 接口参考.docx
data/20260507/华为服务器 iBMC300 Redfish 接口说明.docx
```

输出目录为：

```text
output/20260507/
```

如需指定非默认文件路径：

```bash
python3 scripts/run_pipeline.py 20260507 \
  --podm data/20260507/Atlas PoDManager 1.0.0 Redfish 接口参考.docx \
  --bmc data/20260507/华为服务器 iBMC300 Redfish 接口说明.docx
```

**单独执行某一步**时，不带参数会直接跑默认输入文件：

```bash
# 默认输入见 scripts/_defaults.py
python3 scripts/extract_podm_interface_list.py
python3 scripts/extract_bmc_interface_list.py
python3 scripts/extract_from_tables.py
python3 scripts/extract_from_examples.py
```

**传参数**可处理任何文件：

```bash
python3 scripts/extract_podm_interface_list.py data/你的PoDM文件.docx output/你的PoDM文件.interface-list.yaml
python3 scripts/extract_bmc_interface_list.py  data/你的BMC文件.docx  output/你的BMC文件.interface-list.yaml
python3 scripts/extract_from_tables.py    data/你的文件.docx   output/你的文件.interfaces.yaml
python3 scripts/extract_from_examples.py  data/你的文件.docx   output/你的文件.example.interfaces.yaml
python3 scripts/extract_bmc.py            data/你的BMC文件.docx output/你的BMC文件.bmc.interfaces.yaml
```

只传输入、不传输出时，结果写到约定的默认文件名。

两条接口+参数路径都**同时**产出 `.interfaces.yaml`（结构化参数清单）和 `.uris.txt`
（每行 `[METHOD] URI`，顺序与 yaml 一致），分别给结构化 diff 和纯 URI
集合对比用。

如果要换默认文件名，改 `scripts/_defaults.py` 里的 `PODM_DOCX_NAME` /
`BMC_DOCX_NAME` 常量即可。

## 验证

提交前跑统一检查：

```bash
conda run -n base python scripts/check.py
```

检查内容：

- 编译 `scripts/*.py`
- 运行 `tests/` 下的标准库 `unittest`

## 输出示例

**interface-list.yaml**

```yaml
interfaces:
- index: 1
  section: 3.19.3
  title: 基于SPDM协议获取组件签名测量值
  method: POST
  uri: https://device_ip/redfish/v1/ComponentIntegrity/component_integrity_id/Actions/ComponentIntegrity.SPDMGetSignedMeasurements
```

**interfaces.yaml**

```yaml
interfaces:
  - section: 4.2.25
    title: 导出日志信息
    method: POST
    uri: /redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Actions/Oem/Huawei/LogService.ExportLog
    params:
      path:     [manager_id, logservices_id]
      header:   [X-Auth-Token, Content-Type]
      body:     [Type, Content]
      query:    []
      response: ["@odata.context", "@odata.type", "@odata.id", Id, Name, TaskState, StartTime, Messages, Oem/Huawei, TaskPercentage]
```

## 诊断工具

跑完主工作流如果发现某节漏字段 / 多字段 / 解析错乱，按症状对号：

| 症状 | 用哪个 |
|---|---|
| 某节解析不完整，想看原文长啥样 | `scripts/section_dump.py X.Y.Z` 导出该节扁平化后的原文 |
| 类型词白名单要扩哪些 | `scripts/type_enum.py` 列出"类型"列所有真实取值 + 频次 |
| 怀疑表格某列写法不一致 | `scripts/col_enum.py 1` 列出第 2 列所有取值 |
| 标题识别不全 | `scripts/docx_diag.py` 看段落样式分布 |

## 文档格式假设

脚本按以下规则识别文档结构：

- **章节标题**：`数字.数字[.数字...]` + 空格 + 文本，例如 `4.2.25 导出日志信息`
- **接口小节**：依次使用中文标记 `接口功能` / `调用方法` / `URI` / `请求参数` / `请求示例` / `响应参数` / `响应示例`
- **参数表**：以 `表X-XXX ... 参数列表` 为标题；表头常见列名含 `参数名称` / `必选` / `类型` / `参数值域` / `默认值` / `参数说明`
- 表格行在 Word 导出后以 `\t` 或 2+ 空格分隔；多行单元格的续行自动并入上一行

## 已知限制

- 手动序号的标题（Word 自动编号）在文本中没有 `X.Y.Z` 字样时识别不到。
- 嵌套表（表中套表）可能漏行。
- 旧版 `.doc`（OLE2 二进制）不支持；先用 `libreoffice --headless --convert-to docx` 或 `pandoc` 转成 `.docx`。

## 许可

MIT
