---
name: redfish-interface-match-review
description: Compare BMC and PoDManager Redfish interface-list YAML files using LLM semantic review and consolidated Excel workbooks. Use when asked to judge whether interfaces belong to the same API, summarize common/BMC-only/PoDM-only interfaces, review ambiguous matches, or package dated semantic analysis outputs.
---

# Redfish Interface Match Review

## Purpose

Use this skill for this project's BMC vs PoDManager interface ownership analysis when the user wants model-based semantic judgment rather than a mechanical title-score report.

The expected output is a dated semantic analysis directory containing:

- common interfaces;
- BMC-only interfaces;
- PoDM-only interfaces;
- one Markdown review report;
- one Excel workbook with three sheets.

## Inputs

Default dated inputs:

```text
output/<date>/华为服务器 iBMC300 Redfish 接口说明.interface-list.yaml
output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.interface-list.yaml
```

Expected YAML item fields:

```yaml
index: 1
section: 3.19.3
title: 基于SPDM协议获取组件签名测量值
method: POST
uri: https://device_ip/redfish/v1/...
```

## Workflow

1. Load both `*.interface-list.yaml` files.
2. Build candidate pairs from title, method, normalized URI, URI skeleton, and final Action name.
3. Use LLM semantic judgment to decide one-to-one interface ownership.
4. Write semantic review outputs:

```text
analysis/<date>/llm_interface_match_review.md
analysis/<date>/llm_common_interfaces.yaml
analysis/<date>/llm_bmc_only_interfaces.yaml
analysis/<date>/llm_podm_only_interfaces.yaml
analysis/<date>/llm_common_interfaces.csv
analysis/<date>/llm_bmc_only_interfaces.csv
analysis/<date>/llm_podm_only_interfaces.csv
analysis/<date>/llm_interface_match_review.xlsx
```

5. Export one consolidated Excel workbook with exactly three sheets:

```text
analysis/<date>/llm_interface_match_review.xlsx
  - 共有接口
  - BMC独有
  - PoDM独有
```

If separate per-category Excel files exist after consolidation, delete only those per-category Excel files. Keep CSV/YAML/Markdown source artifacts unless the user explicitly asks to remove them.

## Semantic Review Rules

Judge "same interface" by combining these signals, in this order:

1. Same normalized URI and same method: usually same interface, even when titles differ.
2. Same final Action name and compatible resource path: usually same interface when method also matches.
3. Same resource path skeleton with product terminology differences: likely same interface, mark medium confidence if product concepts differ.
4. Same title but different Action/resource: do not blindly accept; reject or reassign if URI/Action points elsewhere.
5. Same broad domain only: keep as 独有 unless URI/Action or precise operation semantics support a match.

Common synonym/product-normalization examples:

- `截屏` / `截图`
- `上传` / `导入` when Action is the same import operation
- `查询集合资源信息` / `查询全量...`
- `用户服务信息` / `账户策略` when URI is `AccountService`
- `会话服务信息` / `会话策略` when URI is `SessionService`
- `iBMCBMC` / `PoDManager` as product name replacement
- `LCN` / `UBM` as medium-confidence product-term replacement unless URI/Action strongly confirms it

Use `high` confidence when URI or Action directly confirms the match. Use `medium` when the match depends on product terminology or semantic equivalence. Use `low` only when the result intentionally needs human review.

## Report Requirements

The Markdown report must include:

- BMC interface count;
- PoDManager interface count;
- common interface count;
- BMC-only count;
- PoDM-only count;
- notes for medium/low-confidence or non-literal title matches.

Use absolute file links in the final user response for the important reports and Excel files.

## Verification

Run project checks after adding or editing code:

```bash
conda run -n base python scripts/check.py
```

For Excel outputs, reload the workbook and verify:

- sheet names are exactly `共有接口`, `BMC独有`, `PoDM独有`;
- row counts match the source CSV files;
- each workbook contains only the requested three sheets.
