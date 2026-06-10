---
name: redfish-compare-baseline
description: Extract BMC and PoDManager Redfish interfaces from a dated document folder or explicit Word document paths, then compare the new interface-list YAML files against baseline/reviewed_baseline.xlsx by running scripts/update_interface_summary_from_baseline.py. Use when the user invokes /redfish-compare-baseline or asks to generate new_summary.xlsx and interface_update_report.json for a date such as 20260609.
---

# Redfish Compare Baseline

Run extraction and baseline comparison as one independent workflow. Do not call or depend on `redfish-extract-interfaces`; this skill runs `scripts/run_pipeline.py` itself.

## Invocation

Expected user form:

```text
/redfish-compare-baseline 20260609
```

Also accept a dated directory path such as:

```text
/redfish-compare-baseline /path/to/20260609
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, use it as `<date>` and expect documents in `data/<date>/`.
   - If the argument is a directory path, use the directory basename as `<date>` and find the BMC and PoDManager `.docx` files inside that directory.
3. Run the extraction pipeline:

```bash
python scripts/run_pipeline.py <date>
```

For a non-default directory, pass explicit files:

```bash
python scripts/run_pipeline.py <date> \
  --podm "<dir>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc "<dir>/华为服务器 iBMC300 Redfish 接口说明.docx"
```

4. Run the baseline comparison:

```bash
python scripts/update_interface_summary_from_baseline.py <date>
```

The updater uses:

```text
baseline/reviewed_baseline.xlsx
baseline/reviewed_baseline_manifest.json
```

and writes:

```text
output/<date>/analysis/new_summary.xlsx
output/<date>/analysis/interface_update_report.json
```

5. Read `interface_update_report.json` and report the counts for:
   - `summary.common.added/deleted/changed`
   - `summary.bmc_only.added/deleted/changed`
   - `summary.podm_only.added/deleted/changed`
   - `summary.review_needed`

6. Open or inspect `new_summary.xlsx` only if needed. Do not manually redo新增/删除/变更 judgment; the script owns that logic.

## Review Boundary

Manual or AI review is limited to rows already marked by the script:

- `新增`
- `删除`
- `变更`
- `需复核是否可与对端接口配对`

If the extractor produced a wrong URI, fix the generated YAML only with clear source evidence or user confirmation, then rerun this skill's workflow.
