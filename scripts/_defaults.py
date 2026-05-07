"""Project-wide default document names and derived paths."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"
ANALYSIS_DIR = REPO_ROOT / "analysis"

PODM_DOCX_NAME = "Atlas PoDManager 1.0.0 Redfish 接口参考-20260507.docx"
BMC_DOCX_NAME = "华为服务器 iBMC300 Redfish 接口说明-20260507.docx"

PODM_DOCX = DATA_DIR / PODM_DOCX_NAME
BMC_DOCX = DATA_DIR / BMC_DOCX_NAME

PODM_STEM = Path(PODM_DOCX_NAME).stem
BMC_STEM = Path(BMC_DOCX_NAME).stem
