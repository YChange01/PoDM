---
name: redfish-resource-tree-promote-baseline
description: Promote a manually reviewed Redfish resource-tree comparison workbook to baseline/resource_tree_baseline.xlsx and regenerate baseline/resource_tree_baseline_manifest.json by running scripts/promote_resource_tree_baseline.py. Use when the user invokes /redfish-resource-tree-promote-baseline with a date such as 20260609.
---

# Redfish Resource Tree Promote Baseline

Use this only after the user has manually reviewed and accepted a generated `resource_tree_summary.xlsx` as the new resource-tree authority.

## Invocation

Expected user form:

```text
/redfish-resource-tree-promote-baseline 20260609
```

This promotes:

```text
output/20260609/analysis/resource_tree_summary.xlsx
```

Before replacing an existing resource-tree baseline, the script archives previous resource-tree baseline files under:

```text
baseline/backup_resource_tree_<UTC timestamp>/
```

The backup folder contains timestamped copies such as `resource_tree_baseline_<UTC timestamp>.xlsx` and `resource_tree_baseline_manifest_<UTC timestamp>.json`, and the new manifest records the folder path in `previous_baseline_backup`.

Also accept an explicit reviewed workbook path:

```text
/redfish-resource-tree-promote-baseline /path/to/resource_tree_summary.xlsx
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, run:

```bash
python scripts/promote_resource_tree_baseline.py <date>
```

   - If the argument is an `.xlsx` path, run:

```bash
python scripts/promote_resource_tree_baseline.py --source "<reviewed.xlsx>" --baseline-date <date-if-known>
```

3. Verify these files exist and were updated:

```text
baseline/resource_tree_baseline.xlsx
baseline/resource_tree_baseline_manifest.json
```

4. If there was an existing resource-tree baseline, verify the timestamped backup folder exists under `baseline/`.

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
