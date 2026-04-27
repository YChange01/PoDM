# PoDManager 接口文档智能分析 —— AI 辅助实战路径

## 已完成的 8 项分析维度

| # | 分析维度 | 产出文件 |
|---|---|---|
| 1 | **PoDM 表格路径** 接口 / 参数提取 | `output/Atlas PoDManager....interfaces.yaml` |
| 2 | **PoDM 示例路径** 接口 / 参数提取 | `output/Atlas PoDManager....example.interfaces.yaml` |
| 3 | **PoDM 表格 vs 示例** 参数对比（内部一致性）| `output/uri_diff.txt` + `param_diff.txt` |
| 4 | **PoDM 接口 doc bug 汇总报告**（6 大类、~96 条具体 bug） | `analysis/error_cases.md` + `.docx` |
| 5 | **BMC iBMC300 接口 / 参数提取** | `output/华为服务器 iBMC300....bmc.interfaces.yaml` |
| 6 | **PoDM vs BMC URI 跨文档对比**（304 条配对 / 60 条 URI 不一致） | `analysis/cross_doc_diff.md` |
| 7 | **PoDM vs BMC 参数 跨文档对比**（226 条接口逐字段 diff 详情） | `analysis/cross_doc_diff.md` |
| 8 | **PoDM 修订建议清单**（按 BMC 同名接口字段缺失数排序，全量 97 条 + 4 条 method 错误） | `analysis/cross_doc_diff.md` 末段 |

---

## 在本项目中的 [Rule] / [Skill] / [Agent] 含义

> 跟示例项目同款分类，但落在 doc-mining 工作上。

```
 [Rule] —— 始终在背景生效的硬约束（违反会被自动纠正 / 提醒）

    common/coding-style.md  → 文件 < 800 行：extractor 超界后自动拆出
                              _doc_structure.py / _yaml_io.py 共享模块
    common/testing.md       → 改 regex 后必跑 smoke test 9-16 个 case
    common/security.md      → 不归一化原文，忠实输出 doc bug；
                              warning 也写到独立文件，不污染 yaml

    例：marker 正则放宽前先写 16-case fixture 验证不回归

 [Skill] —— 可调用的工作流模板（在本项目落地为脚本化 pipeline）

    extract_from_tables  → 从"请求参数 / 响应参数"抓表格首列
    extract_from_examples → 从"请求示例 / 响应示例"抓 HTTP/JSON
    extract_bmc          → 从 BMC "命令格式 / 输出说明" 抓
    diff_uris            → 同 doc 内 URI 跨视图对比
    diff_params          → 同 doc 内参数跨视图对比
    diff_cross_doc       → 跨文档 BMC vs PoDM 配对 + 字段 diff
    pandoc + reference   → md → docx，宋体 + Times New Roman 排版
    git workflow         → 每个 fix 一个聚焦 commit，message 写明覆盖的 section

    例："修 4.4.7 表4-712 刀片型号被误抓为 body" → 触发 extract_from_tables
        的 iter_tables 加硬停止条件 + 16 case 烟测 + 一个 fix commit

 [Agent] —— 派出去办具体事的角色（在本项目里以函数 / 模块边界呈现）

    Section splitter        → split_sections + dedup_sections（章节切分）
    Marker recognizer       → match_marker（识别子段 marker，含前缀容错）
    Table boundary detector → iter_tables（识别表格边界，硬停止于任何 表X-YYY）
    Param-row classifier    → extract_param_names（用类型列启发式 + 名称正则）
    Cross-doc pair matcher  → pair_interfaces（4 阶段配对：title > uri+method > uri > skeleton）
    Diff renderer           → diff_params / render_report（统一 only_X / common 三态）
    Warning collector       → 整流 silent failure，统一写 *.warnings.txt
```

---

## ① 文档结构识别 / 数据采集阶段

**做什么**：把 docx 转成行级 txt，识别章节 / 子段 / 表格 / JSON 边界。

| 用到的 | 说明 |
|---|---|
| `[Rule]` `coding-style.md` | 共享识别逻辑独立成 `_doc_structure.py`（194 行 < 800 上限），避免 PoDM/BMC 两 extractor 漂移 |
| `[Skill]` `_docx_utils.read_source` | docx → 行级文本 |
| `[Skill]` `extract_headings` | 先看目录，掌握 chapter 3 接口 / chapter 4 附录的边界 |
| `[Agent]` Section splitter | `HEADING_RE` 识别 `\d+(\.\d+)+ + 标题`；标题首字符禁 `/` 但允许内含 `/`（修 4.10.2 "带内升级软件/固件" 标题）|
| `[Agent]` Marker recognizer | `match_marker` 兼容三种写法：基础 / `\s*\d*` 数字带空格（修 4.2.39 "响应参数 1"）/ `\S{1,5}板` 板型前缀（修 4.4.2 "SMN板响应参数"）|

**关键决策**：marker / 表标题正则**单源化**——历史上两个 extractor 各维护一份导致漂移。

---

## ② 解析器实现 / 测试驱动阶段

**做什么**：把识别好的子段映射到 `Interface` 数据类（method / uri / params{path/header/body/query/response}）。

| 用到的 | 说明 |
|---|---|
| `[Rule]` `testing.md` | 每改一个 regex 必跑烟测：marker 9 case、URL 7 case、表标题 9 case |
| `[Rule]` `coding-style.md` | Params/Interface 数据类 + dump_yaml 抽到 `_yaml_io.py`，避免两份 extractor 各写一遍 |
| `[Skill]` `extract_from_tables` | 表格首列识别（类型列启发式 + `_NAME_LIKE_RE`），"无类型列"行用结构补救 |
| `[Skill]` `extract_from_examples` | HTTP 首行宽容正则容文档手滑（`POST/redfish` 缺空格、`/Storage. Import` 中部空格、`...HTTP/1.1` 粘连）+ JSON 平衡括号 + 失败降级正则 |
| `[Skill]` `extract_bmc` | BMC 文档结构差异处理：合并的 `命令格式` / bare 占位符 / 输出说明独立表 |
| `[Agent]` Param-row classifier | 区分参数行 vs 续行（类型命中 + 结构补救双规则）|
| `[Agent]` Table boundary detector | iter_tables 5 个硬停止条件，含 `_ANY_TABLE_HEADER_RE`（修 4.4.7 表4-712 刀片型号污染 body）|

**关键决策**：**忠实抓取，不归一化**——`Manager.Reset` 不擅自加 `#` 前缀，`SubneMask` 不擅自改 `SubnetMask`，让 doc bug 在 diff 阶段集中暴露。

---

## ③ 内部一致性对比 / 错误发现阶段（PoDM 单文档维度）

**做什么**：用同一份 docx 的两个视图（表格 vs 示例）相互校验，定位 doc bug。

| 用到的 | 说明 |
|---|---|
| `[Rule]` `code-review.md` | 看到 4.10.4.2 examples 整条丢弃时，不修 extractor 去掩盖，记 doc bug 案例 E001 |
| `[Skill]` `diff_uris` | URI 不一致 56 条 + method 不一致 5 条，按 8 类标签（NO_LEADING_SLASH / DOUBLE_SLASH / MISSING_BRACES / 等）分类 |
| `[Skill]` `diff_params` | 5 个类别（path/header/body/query/response）逐 section 对比，370 接口里 370 条至少一类有差 |
| `[Skill]` `pandoc` + reference doc | md → docx，宋体 + Times New Roman + 表格头行底纹 |
| `[Agent]` Warning collector | 4.10.4.2 整条丢弃 → 自报到 `*.example.warnings.txt`，不再静默 |

**产出**：`error_cases.md`/`.docx`，6 大类 ~96 条具体 bug + P0/P1/P2/P3 修订优先级矩阵。

---

## ④ 跨文档对比 / 修订建议阶段（BMC vs PoDM 维度）

**做什么**：BMC iBMC300 (542 接口) 和 PoDM (371 接口) 跨文档配对，用 BMC 的字段集帮 PoDM 找漏列。

| 用到的 | 说明 |
|---|---|
| `[Rule]` `patterns.md` | 单源化数据类（`_yaml_io.Interface`），BMC / PoDM extractor 输出同款 yaml schema，diff 工具一份代码同时吃 |
| `[Skill]` `diff_cross_doc` | 4 阶段配对策略 (title > uri+method > uri > skeleton)，避免把 PATCH 接口配到同 URI 的 GET 上 |
| `[Skill]` URI 归一化 | 剥 `https://device_ip` + bare 占位符加 `{}` + 去 query string，让两边 URI 可比 |
| `[Agent]` Cross-doc pair matcher | 304 条匹配成功 (82%)，仅 PoDM 67 条 / 仅 BMC 238 条 |
| `[Agent]` Diff renderer | 226 条参数差异逐条展开（每个 category 列「仅 PoDM」/「仅 BMC」具体字段名）|
| `[Agent]` 修订建议生成 | 全量 97 条 PoDM response 缺字段接口，按缺失数降序，可直接拿来逐条 review |

**产出**：`cross_doc_diff.md` (2827 行) + `cross_doc_diff.docx` (90 KB)。

---

## ⑤ 重构 / 沉淀阶段

**做什么**：随着 fix 累积，把重复逻辑抽成共享模块；docx 报告归档供文档作者直接 review。

| 用到的 | 说明 |
|---|---|
| `[Rule]` `coding-style.md` | refactor commit 一次性把 SECTION_MARKERS、Params、dump_yaml 等 5 处重复抽出 |
| `[Rule]` `git-workflow.md` | 每个 fix 一个聚焦 commit；commit message 写明覆盖的 section / case / 影响接口数 |
| `[Skill]` `update-docs` | `analysis/error_cases.md` 与 `analysis/cross_doc_diff.md` 入库，docx 同款样式 |
| `[Skill]` 反向给文档作者 | docx 直接交付，不用让文档作者读 markdown / yaml |

**关键决策**：`*.docx` 全局 gitignore（防 source spec 入库）+ `!analysis/*.docx` 例外（生成报告允许入库）。

---

## 整体心得

1. **忠实 + 暴露 > 规范化**——extractor 的目标不是修文档，是诚实反映文档现状。所有 doc bug 在 diff/warning 里集中暴露，由人决定怎么改文档。

2. **单源化 = 防漂移**——marker 正则、Interface 数据类只能有一份，否则两个 extractor 永远在分头打补丁。

3. **小步迭代 + 烟测**——每个 regex 修改都先写 9-16 case 烟测，确保新增覆盖不破坏旧 case，让 bug 修复可追溯。

4. **配对 4 阶段优先级**——跨文档 diff 第一版只用 title + uri 两阶段，把 PATCH 接口错配到 GET 上 14 处。加了 `uri+method` 联合配对后误判从 18 降到 4（真实差异）。

5. **每个 silent failure 都要发声**——`warnings.txt` 机制让"被丢弃的接口"立刻可见（24 条 BMC 接口因"新URL：" / "请求命令：URL:" 被漏抓即时发现并修复）。
