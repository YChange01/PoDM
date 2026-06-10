---
name: redfish-extract-interfaces
description: Extract BMC and PoDManager Redfish interface files from a dated document folder or explicit Word document paths by running this repository's scripts/run_pipeline.py. Use when the user invokes /redfish-extract-interfaces or asks to extract BMC/PoDManager interface-list YAML, parameter YAML, URI text, or interface_match_llm_input.md for a date such as 20260609.
---

# Redfish Extract Interfaces

Run only the extraction pipeline. Do not compare with baseline and do not edit Excel files.

## Invocation

Expected user form:

```text
/redfish-extract-interfaces 20260609
```

Also accept a dated directory path such as:

```text
/redfish-extract-interfaces /path/to/20260609
```

## Workflow

1. Work from the repository root.
2. Resolve the input:
   - If the argument is `YYYYMMDD`, use it as `<date>` and expect documents in `data/<date>/`.
   - If the argument is a directory path, use the directory basename as `<date>` and find the BMC and PoDManager `.docx` files inside that directory.
3. Run extraction:

```bash
python scripts/run_pipeline.py <date>
```

For a non-default directory, pass explicit files:

```bash
python scripts/run_pipeline.py <date> \
  --podm "<dir>/Atlas PoDManager 1.0.0 Redfish 接口参考.docx" \
  --bmc "<dir>/华为服务器 iBMC300 Redfish 接口说明.docx"
```

4. Verify the expected outputs exist:

```text
output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.interface-list.yaml
output/<date>/华为服务器 iBMC300 Redfish 接口说明.interface-list.yaml
output/<date>/analysis/interface_match_llm_input.md
output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.interfaces.yaml
output/<date>/Atlas PoDManager 1.0.0 Redfish 接口参考.example.interfaces.yaml
output/<date>/华为服务器 iBMC300 Redfish 接口说明.bmc.interfaces.yaml
```

5. Report the generated paths and any extraction errors. Do not perform semantic matching in this skill.
