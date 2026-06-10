---
name: redfish-resource-tree-compare-baseline
description: Extract PoDManager Redfish resource-tree interfaces, split multi-method rows such as GET/PATCH into separate interfaces, compare them with the PoDManager interface-list YAML and the optional baseline/resource_tree_baseline.xlsx, then generate resource_tree_summary.xlsx and resource_tree_update_report.json. Use when the user invokes /redfish-resource-tree-compare-baseline with a date such as 20260609.
---

# Redfish Resource Tree Compare Baseline

Run PoDManager interface-list extraction, resource-tree extraction, and resource-tree baseline comparison as one workflow. This workflow does not require a BMC document.

## Invocation

Expected user form:

```text
/redfish-resource-tree-compare-baseline 20260609
```

Also accept a dated directory path such as:

```text
/redfish-resource-tree-compare-baseline /path/to/20260609
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, use documents in `data/<date>/`.
   - If the argument is a directory path, use the directory basename as `<date>` and find the PoDManager `.docx` file inside it.
3. Extract the PoDManager interface-list YAML:

```bash
python scripts/extract_podm_interface_list.py \
  "data/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  "output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.interface-list.yaml"
```

4. Extract the resource-tree interface-list YAML:

```bash
python scripts/extract_resource_tree_interfaces.py <date>
```

The extractor splits rows such as `GET/POST`, `GET/DELETE`, and `GET/PATCH/DELETE` into separate method+URI interfaces. Blank allowed-operation rows are not counted as interfaces.

5. Compare resource-tree YAML with PoDManager interface-list YAML and the resource-tree baseline:

```bash
python scripts/update_resource_tree_summary_from_baseline.py <date>
```

For a non-default document name or directory, pass explicit YAML/output paths:

```bash
python scripts/update_resource_tree_summary_from_baseline.py \
  --resource-tree-yaml "<resource-tree-yaml>" \
  --podm-yaml "<podm-interface-list-yaml>" \
  --output "output/<date>/analysis/resource_tree_summary.xlsx"
```

The updater uses `baseline/resource_tree_baseline.xlsx` and `baseline/resource_tree_baseline_manifest.json` when they exist. If no resource-tree baseline exists, it still creates an initial direct comparison.

Outputs:

```text
output/<date>/analysis/resource_tree_summary.xlsx
output/<date>/analysis/resource_tree_update_report.json
```

6. Read `resource_tree_update_report.json` and report counts for:
   - `summary.common.added/deleted/changed`
   - `summary.resource_tree_only.added/deleted/changed`
   - `summary.podm_only.added/deleted/changed`
   - `summary.review_needed`

Do not manually redo新增/删除/变更 judgment; the script owns that logic.
