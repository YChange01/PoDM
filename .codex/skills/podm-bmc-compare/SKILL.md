---
name: podm-bmc-compare
description: Extract PoDManager and BMC Redfish interface lists from a dated document folder or explicit Word document paths, then compare them against baseline/podm_bmc/baseline.xlsx by running scripts/compare_podm_bmc_to_baseline.py. Use when the user invokes /podm-bmc-compare or asks to generate podm_bmc_summary.xlsx and podm_bmc_update_report.json for a date such as 20260609.
---

# PoDM-BMC Compare

Run PoDManager-vs-BMC extraction and baseline comparison as one independent workflow.

## Invocation

```text
/podm-bmc-compare 20260609
```

Also accept a dated directory path such as:

```text
/podm-bmc-compare /path/to/20260609
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, use `data/<date>/`.
   - If the argument is a directory path, use the directory basename as `<date>` and find the BMC and PoDManager `.docx` files inside that directory.
3. Run the extraction pipeline:

```bash
python scripts/run_podm_bmc_pipeline.py <date>
```

For a non-default directory, pass explicit files:

```bash
python scripts/run_podm_bmc_pipeline.py <date> \
  --podm "<dir>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc "<dir>/华为服务器 iBMC300 Redfish 接口说明.docx"
```

4. Run the baseline comparison:

```bash
python scripts/compare_podm_bmc_to_baseline.py <date>
```

The updater uses:

```text
baseline/podm_bmc/baseline.xlsx
baseline/podm_bmc/manifest.json
```

and writes:

```text
output/<date>/analysis/podm_bmc_summary.xlsx
output/<date>/analysis/podm_bmc_update_report.json
```

5. Read `podm_bmc_update_report.json` and report:
   - `summary.common.added/deleted/changed`
   - `summary.bmc_only.added/deleted/changed`
   - `summary.podm_only.added/deleted/changed`
   - `summary.review_needed`

Do not manually redo新增/删除/变更 judgment; the script owns that logic.
