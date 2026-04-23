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
│   ├── extract_headings.py
│   └── extract_interfaces.py
├── data/             # 放原始文档（.docx / .txt），本地使用，不入库
└── output/           # 脚本生成的结果（headings.txt / interfaces.yaml），不入库
```

`data/` 与 `output/` 目录保留空壳（`.gitkeep`），内部文件默认被 `.gitignore` 屏蔽。

## 工具

| 脚本 | 作用 | 默认输出 |
|---|---|---|
| `scripts/extract_headings.py` | 提取 `X.Y.Z` 级章节标题，每个接口小节附带 `[METHOD] URI` | `<input>.headings.txt` |
| `scripts/extract_interfaces.py` | 按接口小节提取 URI + 各表第一列（参数名称），分 path/header/body/query/response | `<input>.interfaces.yaml` |

## 用法

把原始文档放到 `data/`，输出落在 `output/`：

```bash
# 标题树
python3 scripts/extract_headings.py   data/PoDM_API.docx   output/PoDM_API.headings.txt

# 接口参数
python3 scripts/extract_interfaces.py data/PoDM_API.docx   output/PoDM_API.yaml

# 也可指定 JSON 输出
python3 scripts/extract_interfaces.py data/PoDM_API.docx   output/PoDM_API.json --format json
```

不带第二个参数时，输出会写到与输入同名的 `.headings.txt` / `.interfaces.yaml`。

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
