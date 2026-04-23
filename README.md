# PoDM 接口文档提取工具

从 Redfish 接口文档（Word `.docx` 或纯文本 `.txt`）中提取章节结构与接口参数，
方便后续做跨版本 / 跨产品（如 BMC vs PoDM）的对比分析。

> 零第三方依赖：仅用 Python 3 标准库（`zipfile` + `xml.etree`）直读 `.docx`，
> 不需要 `pandoc` / `python-docx` / `pip` 安装。
> 若安装了 `PyYAML`，`extract_interfaces.py` 会用 YAML 输出，否则自动回退 JSON。

## 目录结构

```
PoDM/
├── README.md
├── .gitignore
├── scripts/          # 公共提取工具
│   ├── _docx_utils.py
│   ├── docx_diag.py
│   ├── extract_headings.py
│   ├── extract_interfaces.py
│   └── extract_uris.py
├── analysis/         # 一次性对比分析（BMC vs PoDM 的 Redfish 接口清单）
│   ├── compare.py              # 规范化 URI 后做集合差/分类汇总
│   ├── compare_report.txt      # 脚本输出：按分类列出共同/独有接口
│   └── BMC_vs_PoDM_分析.txt    # 基于 compare 结果的人肉分析
├── data/             # 放原始文档（.docx / .txt），本地使用，不入库
└── output/           # 脚本生成的结果（headings.txt / interfaces.yaml），不入库
```

`data/` 与 `output/` 目录只保留空壳（`.gitkeep`），内部文件默认被 `.gitignore` 屏蔽。
`analysis/compare.py` 依赖 `data/BMC.txt` 和 `data/PoDM.txt` 运行，公开仓库里跑
不起来是预期的——报告本身可读即可。

## 工具

| 脚本 | 作用 | 默认输出 |
|---|---|---|
| `scripts/extract_headings.py` | 提取 `X.Y.Z` 级章节标题，每个接口小节附带 `[METHOD] URI` | `<input>.headings.txt` |
| `scripts/extract_interfaces.py` | 按接口小节提取 URI + 各表第一列（参数名称），分 path/header/body/query/response | `<input>.interfaces.yaml` |
| `scripts/extract_uris.py` | 从已生成的 `headings.txt` 里只抽出 URI，每行一个（顺序保留，不去重） | `<input>.uris.txt` |
| `scripts/docx_diag.py` | 打印 `.docx` 里段落样式分布 + 首次文本样本，排查非标准样式用 | stdout |

## 用法

把原始文档放到 `data/`，输出落在 `output/`。

**不带参数**会直接跑仓库默认的输入文件（写死在脚本里），输出到 `output/` 下：

```bash
# 默认输入：data/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx
# 默认输出：output/<输入文件名>.headings.txt   /   .interfaces.yaml
python3 scripts/extract_headings.py
python3 scripts/extract_interfaces.py
```

**传参数**可处理任何文件：

```bash
python3 scripts/extract_headings.py   data/你的文件.docx   output/你的文件.headings.txt
python3 scripts/extract_interfaces.py data/你的文件.docx   output/你的文件.interfaces.yaml
```

只传输入、不传输出时，结果写到与输入同名的 `.headings.txt` / `.interfaces.yaml`。

**从 headings.txt 再抽出纯 URI 列表**：

```bash
python3 scripts/extract_uris.py                                   # 默认读 output/<默认文件>.headings.txt
python3 scripts/extract_uris.py output/你的文件.headings.txt        # 指定输入
```

如果要换默认输入，改 `scripts/extract_*.py` 里的 `DEFAULT_INPUT` 常量即可。

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
    uri: /redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Actions/Oem/Huawei/LogService.ExportLog
    params:
      path:     [manager_id, logservices_id]
      header:   [X-Auth-Token, Content-Type]
      body:     [Type, Content]
      query:    []
      response: ["@odata.context", "@odata.type", "@odata.id", Id, Name, TaskState, StartTime, Messages, Oem/Huawei, TaskPercentage]
```

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
