---
name: podm-bmc-compare
description: One-step PoDManager-vs-BMC Redfish workflow for a date such as /podm-bmc-compare 20260609: run scripts/compare_podm_bmc_to_baseline.py <date>, which auto-runs scripts/run_podm_bmc_pipeline.py if output/<date>/bmc.interface-list.yaml or podm.interface-list.yaml is missing, then writes podm_bmc_summary.xlsx and podm_bmc_update_report.json.
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
3. For normal date mode, run the compare script directly:

```bash
python scripts/compare_podm_bmc_to_baseline.py <date>
```

The compare script automatically runs the extraction pipeline first if either default YAML is missing:

```text
output/<date>/bmc.interface-list.yaml
output/<date>/podm.interface-list.yaml
```

4. For a non-default document directory, run the extraction pipeline with explicit files, then run compare:

```bash
python scripts/run_podm_bmc_pipeline.py <date> \
  --podm "<dir>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc "<dir>/华为服务器 iBMC300 Redfish 接口说明.docx"

python scripts/compare_podm_bmc_to_baseline.py <date>
```

5. If custom YAML paths are required, pass them explicitly:

```bash
python scripts/compare_podm_bmc_to_baseline.py <date> \
  --bmc-yaml "<path>/bmc.interface-list.yaml" \
  --podm-yaml "<path>/podm.interface-list.yaml"
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

6. Read `podm_bmc_update_report.json` and report:
   - `summary.common.added/deleted/changed`
   - `summary.bmc_only.added/deleted/changed`
   - `summary.podm_only.added/deleted/changed`
   - `summary.review_needed`

Do not manually redo新增/删除/变更 judgment; the script owns that logic.
