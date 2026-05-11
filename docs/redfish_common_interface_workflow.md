# BMC 与 PoDManager Redfish 接口分析流程

本文档描述从两份最新 Word 接口文档开始，按顺序完成接口提取、共有/独有接口判断、共有接口参数提取、参数差异分析的流程。

## 0. 准备输入文档

推荐按日期放置原始 Word 文档：

```text
data/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx
data/<date>/华为服务器 iBMC300 Redfish 接口说明.docx
```

其中 `<date>` 使用 `YYYYMMDD`，例如 `20260511`。

如果文件名或目录不同，后续命令可用 `--podm-doc`、`--bmc-doc` 指定。

## 1. 提取接口清单

运行：

```bash
python scripts/extract_interface_lists.py <date>
```

Windows PowerShell 可用：

```powershell
python .\scripts\extract_interface_lists.py <date>
```

如果文档不在默认位置：

```bash
python scripts/extract_interface_lists.py <date> \
  --podm-doc "path/to/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc-doc "path/to/华为服务器 iBMC300 Redfish 接口说明.docx"
```

输出：

```text
output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.interface-list.yaml
output/<date>/华为服务器 iBMC300 Redfish 接口说明.interface-list.yaml
output/<date>/analysis/interface_match_llm_input.md
```

`interface-list.yaml` 每条接口包含：

```yaml
index: 1
section: 3.1.1
title: 查询Redfish版本信息
method: GET
uri: https://device_ip/redfish
```

## 2. 人工复制接口提取结果

打开并复制：

```text
output/<date>/analysis/interface_match_llm_input.md
```

把该文件内容交给大模型，用于判断共有接口、BMC 独有接口、PoDM 独有接口。

## 3. 大模型分析共有接口和独有接口

大模型分析时要求：

- 基于 `method`、`uri`、URI skeleton、Action 名称和接口语义判断。
- 共有接口必须一对一匹配。
- 不只按标题相似度判断。
- 输出一个 Excel 文件：`interface_match_llm_summary.xlsx`。
- Excel 必须包含且仅包含三个 sheet：
  - `共有接口`
  - `BMC独有`
  - `PoDM独有`

`共有接口` sheet 建议列：

```text
category, confidence, title_similarity_score, method_same,
bmc_index, bmc_section, bmc_title, bmc_method, bmc_uri,
podm_index, podm_section, podm_title, podm_method, podm_uri
```

把大模型产出的 Excel 保存到：

```text
output/<date>/analysis/interface_match_llm_summary.xlsx
```

## 4. 提取共有接口参数

运行：

```bash
python scripts/extract_common_word_interface_params.py <date>
```

Windows PowerShell 可用：

```powershell
python .\scripts\extract_common_word_interface_params.py <date>
```

如果文档或匹配结果不在默认位置：

```bash
python scripts/extract_common_word_interface_params.py <date> \
  --podm-doc "path/to/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc-doc "path/to/华为服务器 iBMC300 Redfish 接口说明.docx" \
  --match-workbook "output/<date>/analysis/interface_match_llm_summary.xlsx"
```

输出：

```text
output/<date>/bmc.common.word.interface-params.yaml
output/<date>/podm.common.word.interface-params.yaml
output/<date>/analysis/common_interface_param_compare_input.md
```

参数输出只保留 `name` 和 `type`：

```yaml
params:
  path:
  - name: manager_id
    type: string
  body:
  - name: Type
    type: string
```

## 5. 人工复制共有接口参数提取结果

打开并复制：

```text
output/<date>/analysis/common_interface_param_compare_input.md
```

该文件包含：

- `interface_match_llm_summary.xlsx` 中 `共有接口` sheet 的配对关系；
- BMC 共有接口参数 YAML；
- PoDManager 共有接口参数 YAML。

## 6. 大模型分析共有接口参数差异

让大模型按共有接口配对关系逐对比较参数，只比较参数 `name` 和 `type`。

建议输出 Excel：

```text
output/<date>/analysis/common_interface_param_diff_llm_summary.xlsx
```

建议列：

```text
bmc_section, bmc_title, podm_section, podm_title,
category, param_name, bmc_type, podm_type, difference_type, notes
```

推荐差异类型：

```text
same
type_diff
only_in_bmc
only_in_podm
category_diff
need_review
```

## 常用命令汇总

```bash
# 1. 提取接口清单
python scripts/extract_interface_lists.py <date>

# 2-3. 复制 output/<date>/analysis/interface_match_llm_input.md 给大模型，
#      保存结果为 output/<date>/analysis/interface_match_llm_summary.xlsx

# 4. 提取共有接口参数
python scripts/extract_common_word_interface_params.py <date>

# 5-6. 复制 output/<date>/analysis/common_interface_param_compare_input.md 给大模型，
#      保存结果为 output/<date>/analysis/common_interface_param_diff_llm_summary.xlsx
```

## 注意事项

- `data/` 和 `output/` 默认被 `.gitignore` 忽略，适合存放本地原始文档和分析产物。
- 如果 Windows 上 `python` 不可用，可尝试 `py -3` 替代。
- 如果读取 `xlsx` 报缺少 `openpyxl`，先安装：

```bash
python -m pip install openpyxl
```
