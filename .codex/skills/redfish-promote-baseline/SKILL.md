---
name: redfish-promote-baseline
description: Promote a manually reviewed Redfish comparison Excel workbook to baseline/reviewed_baseline.xlsx and regenerate baseline/reviewed_baseline_manifest.json by running scripts/promote_reviewed_baseline.py. Use when the user invokes /redfish-promote-baseline with a date such as 20260609 or asks to update the reviewed baseline from an approved new_summary.xlsx.
---

# Redfish Promote Baseline

Use this only after the user has manually reviewed and accepted a generated `new_summary.xlsx` as the new authority.

## Invocation

Expected user form:

```text
/redfish-promote-baseline 20260609
```

This promotes:

```text
output/20260609/analysis/new_summary.xlsx
```

Before replacing an existing baseline, the script archives the previous baseline files under:

```text
baseline/backup_<UTC timestamp>/
```

The backup folder contains timestamped copies such as `reviewed_baseline_<UTC timestamp>.xlsx` and `reviewed_baseline_manifest_<UTC timestamp>.json`, and the new manifest records the folder path in `previous_baseline_backup`.

Also accept an explicit reviewed workbook path:

```text
/redfish-promote-baseline /path/to/new_summary.xlsx
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, run:

```bash
python scripts/promote_reviewed_baseline.py <date>
```

   - If the argument is an `.xlsx` path, run:

```bash
python scripts/promote_reviewed_baseline.py --source "<reviewed.xlsx>" --baseline-date <date-if-known>
```

3. Verify these files exist and were updated:

```text
baseline/reviewed_baseline.xlsx
baseline/reviewed_baseline_manifest.json
```

4. If there was an existing baseline, verify the timestamped backup folder exists under `baseline/`.

5. Read the manifest and report:
   - `baseline_date`
   - `sha256`
   - `previous_baseline_backup`
   - row counts per sheet

6. Run:

```bash
python scripts/check.py
```

Do not hand-edit the manifest hash.
