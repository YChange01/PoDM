# Redfish 接口对比快速说明

本文只保留日常操作需要知道的目录、skill、baseline 和回退方法。

## 目录

在仓库根目录执行命令。

```text
data/<date>/                         # 原始 Word 文档，不入库
output/<date>/                       # 脚本生成结果，不入库
output/<date>/analysis/              # 对比 Excel 和 JSON 报告，不入库
baseline/podm_bmc/                   # PoDM vs BMC 人工确认基线，入库
baseline/podm_resource_tree/         # PoDM vs 资源树人工确认基线，入库
.codex/skills/                       # 项目内置 skills
scripts/                             # skills 实际调用的脚本
```

默认输入文件放在：

```text
data/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx
data/<date>/华为服务器 iBMC300 Redfish 接口说明.docx
```

## Skills

支持项目本地 skill 的 AI 工具，在仓库根目录直接调用：

```text
/podm-bmc-compare 20260609
/podm-bmc-promote 20260609
/podm-tree-compare 20260609
/podm-tree-promote 20260609
```

含义：

- `/podm-bmc-compare <date>`：提取 PoDM/BMC 接口并对比 `baseline/podm_bmc/baseline.xlsx`。如果默认 YAML 不存在，compare 脚本会自动先跑提取流水线。
- `/podm-bmc-promote <date>`：把人工审核后的 `output/<date>/analysis/podm_bmc_summary.xlsx` 提升为 PoDM/BMC baseline。
- `/podm-tree-compare <date>`：提取 PoDM 接口和资源树接口，并对比 `baseline/podm_resource_tree/baseline.xlsx`。
- `/podm-tree-promote <date>`：把人工审核后的 `output/<date>/analysis/podm_resource_tree_summary.xlsx` 提升为资源树 baseline。

如果 AI 工具不识别 skill，就直接执行对应脚本：

```bash
python3 scripts/compare_podm_bmc_to_baseline.py 20260609
python3 scripts/promote_podm_bmc_baseline.py 20260609
python3 scripts/compare_podm_resource_tree_to_baseline.py 20260609
python3 scripts/promote_podm_resource_tree_baseline.py 20260609
```

## 人工审核流程

1. 运行 compare skill。
2. 打开 `output/<date>/analysis/*.xlsx`，人工确认备注和配对。
3. 确认无误后运行 promote skill。
4. promote 会更新当前 baseline，并把旧 baseline 备份到 `backups/<UTC时间戳>/`。
5. 提交前运行检查：

```bash
python3 scripts/check.py
```

## Baseline

当前生效基线：

```text
baseline/podm_bmc/baseline.xlsx
baseline/podm_bmc/manifest.json
baseline/podm_resource_tree/baseline.xlsx
baseline/podm_resource_tree/manifest.json
```

`baseline.xlsx` 是人工确认后的标准版本；`manifest.json` 记录 baseline 路径、SHA256、来源文件和上一次备份位置。不要手工改 manifest，promote 脚本会自动更新。

## 回退

备份位置：

```text
baseline/podm_bmc/backups/<timestamp>/baseline_<timestamp>.xlsx
baseline/podm_resource_tree/backups/<timestamp>/baseline_<timestamp>.xlsx
```

回退时用备份 workbook 重新 promote：

```bash
python3 scripts/promote_podm_bmc_baseline.py \
  --source baseline/podm_bmc/backups/<timestamp>/baseline_<timestamp>.xlsx \
  --baseline-date <date-or-restore-note>

python3 scripts/promote_podm_resource_tree_baseline.py \
  --source baseline/podm_resource_tree/backups/<timestamp>/baseline_<timestamp>.xlsx \
  --baseline-date <date-or-restore-note>
```

这样会保留当前 baseline 的新备份，并重新生成 manifest。

## Git 注意事项

- `baseline/` 入库，`data/` 和 `output/` 默认不入库。
- 本地 promote 后先 `git status`，确认 baseline 和 manifest 有变更。
- `git pull` 前不要留未提交 baseline；先 commit，或确认不需要本地改动。
- `.xlsx` 是二进制文件，远端和本地同时改 baseline 时容易冲突，需要明确选择保留哪一版。
- 不要用 `git reset --hard` 处理 baseline 问题，除非已经确认本地改动可以丢弃。
