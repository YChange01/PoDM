#!/usr/bin/env bash
set -euo pipefail

DATE="${1:-20260507}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

PODM_DOC="${PODM_DOC:-${ROOT_DIR}/data/${DATE}/Atlas PoDManager 1.0.0 Redfish 接口参考.docx}"
BMC_DOC="${BMC_DOC:-${ROOT_DIR}/data/${DATE}/华为服务器 iBMC300 Redfish 接口说明.docx}"
MATCH_WORKBOOK="${MATCH_WORKBOOK:-${ROOT_DIR}/output/${DATE}/analysis/interface_match_llm_summary.xlsx}"
OUT_DIR="${OUT_DIR:-${ROOT_DIR}/output/${DATE}}"

mkdir -p "${OUT_DIR}"

for required in "${PODM_DOC}" "${BMC_DOC}" "${MATCH_WORKBOOK}"; do
  if [[ ! -f "${required}" ]]; then
    echo "missing required file: ${required}" >&2
    exit 1
  fi
done

python3 "${SCRIPT_DIR}/extract_word_interface_params.py" \
  --profile bmc \
  --match-workbook "${MATCH_WORKBOOK}" \
  --match-side bmc \
  "${BMC_DOC}" \
  -o "${OUT_DIR}/bmc.common.word.interface-params.yaml"

python3 "${SCRIPT_DIR}/extract_word_interface_params.py" \
  --profile podm \
  --match-workbook "${MATCH_WORKBOOK}" \
  --match-side podm \
  "${PODM_DOC}" \
  -o "${OUT_DIR}/podm.common.word.interface-params.yaml"
