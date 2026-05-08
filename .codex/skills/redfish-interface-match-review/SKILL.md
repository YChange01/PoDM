---
name: redfish-interface-match-review
description: Compare BMC and PoDManager Redfish interface-list YAML files using direct LLM semantic judgment and a single consolidated Excel workbook. Use when asked to judge whether interfaces belong to the same API by title similarity and API/interface name semantics, summarize common/BMC-only/PoDM-only interfaces, or write dated results under the output analysis folder.
---

# Redfish Interface Match Review

## Purpose

Use this skill for this project's BMC vs PoDManager interface ownership analysis when the user wants direct model-based semantic judgment. Do not implement or run a matching script for the judgment step unless the user explicitly asks for an automation tool.

The expected output is one dated output analysis directory containing:

- common interfaces;
- BMC-only interfaces;
- PoDM-only interfaces;
- one consolidated Excel workbook with three sheets.

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
2. Compare interfaces directly with LLM judgment based on title similarity, API/interface name semantics, method, URI, URI skeleton, and final Action name.
3. Enforce one-to-one pairing: one BMC interface can belong to at most one PoDManager interface, and one PoDManager interface can belong to at most one BMC interface.
4. Write the result under the dated output analysis folder:

```text
output/<date>/analysis/
```

5. Export exactly one consolidated Excel workbook with three sheets:

```text
output/<date>/analysis/interface_match_llm_summary.xlsx
  - 共有接口
  - BMC独有
  - PoDM独有
```

Do not claim a CSV can contain sheets. CSV is flat; use `.xlsx` when the user asks for one file with multiple sheets. If a temporary CSV is useful for staging, keep it only when the user asks for CSV output; otherwise delete it after the workbook is verified.

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

## Workbook Requirements

The Excel workbook must have exactly these sheets:

- `共有接口`
- `BMC独有`
- `PoDM独有`

Recommended columns for `共有接口`:

```text
category, confidence, title_similarity_score, method_same,
bmc_index, bmc_section, bmc_title, bmc_method, bmc_uri,
podm_index, podm_section, podm_title, podm_method, podm_uri
```

For the two 独有 sheets, keep the same columns for consistency and leave the missing side blank.

In the final user response, report the three category counts and link to the `.xlsx` file.

## Verification

Run project checks after adding or editing code:

```bash
conda run -n base python scripts/check.py
```

For Excel outputs, reload the workbook and verify:

- sheet names are exactly `共有接口`, `BMC独有`, `PoDM独有`;
- row counts match the semantic result counts;
- each workbook contains only the requested three sheets.
