---
name: podm-tree-compare
description: Extract PoDManager Redfish resource-tree interfaces, split multi-method rows such as GET/PATCH into separate interfaces, compare them with the PoDManager interface-list YAML and baseline/podm_resource_tree/baseline.xlsx, then generate podm_resource_tree_summary.xlsx and podm_resource_tree_update_report.json. Use when the user invokes /podm-tree-compare with a date such as 20260609.
---

# PoDM-Resource-Tree Compare

Run PoDManager interface-list extraction, resource-tree extraction, and resource-tree baseline comparison as one workflow. This workflow does not require a BMC document.

## Invocation

```text
/podm-tree-compare 20260609
```

Also accept a dated directory path such as:

```text
/podm-tree-compare /path/to/20260609
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
  "output/<date>/podm.interface-list.yaml"
```

4. Extract the resource-tree interface-list YAML:

```bash
python scripts/extract_podm_resource_tree_interface_list.py <date>
```

The extractor splits rows such as `GET/POST`, `GET/DELETE`, and `GET/PATCH/DELETE` into separate method+URI interfaces. Blank allowed-operation cells inherit the previous non-empty operation because the source Word table uses vertically merged cells.

5. Compare resource-tree YAML with PoDManager interface-list YAML and the resource-tree baseline:

```bash
python scripts/compare_podm_resource_tree_to_baseline.py <date>
```

The updater uses:

```text
baseline/podm_resource_tree/baseline.xlsx
baseline/podm_resource_tree/manifest.json
```

and writes:

```text
output/<date>/analysis/podm_resource_tree_summary.xlsx
output/<date>/analysis/podm_resource_tree_update_report.json
```

6. Read `podm_resource_tree_update_report.json` and report:
   - `summary.common.added/deleted/changed`
   - `summary.resource_tree_only.added/deleted/changed`
   - `summary.podm_only.added/deleted/changed`
   - `summary.review_needed`

Do not manually redo新增/删除/变更 judgment; the script owns that logic.
