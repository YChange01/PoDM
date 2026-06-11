---
name: podm-bmc-promote
description: Promote a manually reviewed PoDManager-vs-BMC comparison workbook to baseline/podm_bmc/baseline.xlsx and regenerate baseline/podm_bmc/manifest.json by running scripts/promote_podm_bmc_baseline.py. Use when the user invokes /podm-bmc-promote with a date such as 20260609.
---

# PoDM-BMC Promote

Use this only after the user has manually reviewed and accepted `podm_bmc_summary.xlsx` as the new PoDManager-vs-BMC authority.

## Invocation

```text
/podm-bmc-promote 20260609
```

This promotes:

```text
output/20260609/analysis/podm_bmc_summary.xlsx
```

Before replacing an existing baseline, the script archives previous files under:

```text
baseline/podm_bmc/backups/<UTC timestamp>/
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, run:

```bash
python scripts/promote_podm_bmc_baseline.py <date>
```

   - If the argument is an `.xlsx` path, run:

```bash
python scripts/promote_podm_bmc_baseline.py --source "<reviewed.xlsx>" --baseline-date <date-if-known>
```

3. Verify these files exist and were updated:

```text
baseline/podm_bmc/baseline.xlsx
baseline/podm_bmc/manifest.json
```

4. Read the manifest and report `baseline_date`, `sha256`, `previous_baseline_backup`, and row counts per sheet.
5. Run:

```bash
python scripts/check.py
```

Do not hand-edit the manifest hash.
