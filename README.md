# PoDM 接口文档提取工具

从 Redfish 接口文档（Word `.docx` 或纯文本 `.txt`）中提取章节结构与接口参数，
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
├── scripts/
│   ├── _docx_utils.py                # 共享 .docx 读取 (跳 ToC + 合成 X.Y.Z 编号)
│   ├── extract_headings.py           # 提取章节标题 + [METHOD] URI 的层级树
│   ├── extract_from_tables.py        # 路径①：从表格提取 URI + 参数 (同时产出 uris.txt)
│   ├── extract_from_examples.py      # 路径②：从示例代码提取 URI + 参数 (同时产出 uris.txt)
│   ├── col_enum.py                   # 诊断：按列索引枚举表格某列取值
│   ├── type_enum.py                  # 诊断：枚举参数表"类型"列的取值
│   ├── docx_diag.py                  # 诊断：打印段落样式分布
│   └── section_dump.py               # 诊断：导出指定章节的原文
├── analysis/                         # 一次性对比分析 (BMC vs PoDM)
│   ├── compare.py
│   ├── compare_report.txt
│   └── BMC_vs_PoDM_分析.txt
├── data/                             # 原始文档（.docx / .txt），不入库
└── output/                           # 脚本生成的结果，不入库
```

`data/` 与 `output/` 目录只保留空壳（`.gitkeep`），内部文件默认被 `.gitignore` 屏蔽。
`analysis/compare.py` 依赖 `data/BMC.txt` 和 `data/PoDM.txt` 运行，公开仓库里跑
不起来是预期的——报告本身可读即可。

## 主工作流

| 脚本 | 作用 | 默认输出 |
|---|---|---|
| `scripts/extract_headings.py` | 提取 `X.Y.Z` 级章节标题，每个接口小节附带 `[METHOD] URI`（层级树视图） | `<input>.headings.txt` |
| `scripts/extract_from_tables.py` | **表格路径**：从参数表抽 URI + path/header/body/query/response | `<input>.interfaces.yaml` + `<input>.uris.txt` |
| `scripts/extract_from_examples.py` | **示例路径**：从请求/响应示例代码抽相同字段结构 | `<input>.example.interfaces.yaml` + `<input>.example.uris.txt` |

## 用法

把原始文档放到 `data/`，输出落在 `output/`。

**不带参数**会直接跑仓库默认的输入文件（写死在脚本里），输出到 `output/` 下：

```bash
# 默认输入：data/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx
python3 scripts/extract_headings.py
python3 scripts/extract_from_tables.py
python3 scripts/extract_from_examples.py
```

**传参数**可处理任何文件：

```bash
python3 scripts/extract_headings.py       data/你的文件.docx   output/你的文件.headings.txt
python3 scripts/extract_from_tables.py    data/你的文件.docx   output/你的文件.interfaces.yaml
python3 scripts/extract_from_examples.py  data/你的文件.docx
```

只传输入、不传输出时，结果写到约定的默认文件名。

两条主路径都**同时**产出 `.interfaces.yaml`（结构化参数清单）和 `.uris.txt`
（每行 `[METHOD] URI`，顺序与 yaml 一致），分别给结构化 diff 和纯 URI
集合对比用。

如果要换默认输入，改 `scripts/extract_from_*.py` 里的 `DEFAULT_INPUT` 常量即可。

## 输出示例

**headings.txt**

```
    4.2.25 导出日志信息
        [POST] /redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Actions/Oem/Huawei/LogService.ExportLog
    4.2.26 查询日志集合资源信息
        [GET] /redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Entries
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
