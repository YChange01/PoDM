#!/usr/bin/env python3
"""Run common-interface parameter extraction for BMC and PoDManager documents.

This is a cross-platform replacement for shell-specific wrappers. It calls
`extract_word_interface_params.py` twice: once for the BMC document and once for
the PoDManager document, using the common-interface match workbook as the
section filter.

Usage:
    python scripts/extract_common_word_interface_params.py
    python scripts/extract_common_word_interface_params.py 20260507
    python scripts/extract_common_word_interface_params.py --date 20260507
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_DATE = "20260507"
PODM_DOC_NAME = "Atlas PoDManager 1.0.0 Redfish 接口参考.docx"
BMC_DOC_NAME = "华为服务器 iBMC300 Redfish 接口说明.docx"

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
EXTRACTOR = SCRIPT_DIR / "extract_word_interface_params.py"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="提取 BMC/PoDM 共有接口的接口参数和参数类型"
    )
    parser.add_argument(
        "date_arg",
        nargs="?",
        help=f"日期目录，例如 20260507；默认 {DEFAULT_DATE}",
    )
    parser.add_argument(
        "--date",
        dest="date_opt",
        help=f"日期目录，例如 20260507；默认 {DEFAULT_DATE}",
    )
    parser.add_argument("--podm-doc", type=Path, help="PoDManager Word 文档路径")
    parser.add_argument("--bmc-doc", type=Path, help="BMC Word 文档路径")
    parser.add_argument("--match-workbook", type=Path, help="共有接口匹配 Excel 路径")
    parser.add_argument("--out-dir", type=Path, help="输出目录")
    return parser.parse_args(argv)


def choose_date(args: argparse.Namespace) -> str:
    if args.date_opt:
        return args.date_opt
    if args.date_arg:
        return args.date_arg
    return DEFAULT_DATE


def choose_path(cli_value: Path | None, env_name: str, default: Path) -> Path:
    if cli_value is not None:
        return cli_value
    env_value = os.environ.get(env_name)
    if env_value:
        return Path(env_value)
    return default


def require_files(paths: list[Path]) -> None:
    missing = [path for path in paths if not path.is_file()]
    if missing:
        lines = "\n  ".join(str(path) for path in missing)
        raise SystemExit(f"输入文件不存在:\n  {lines}")


def run_extractor(
    profile: str,
    match_side: str,
    input_doc: Path,
    match_workbook: Path,
    output_path: Path,
) -> None:
    command = [
        sys.executable,
        str(EXTRACTOR),
        "--profile",
        profile,
        "--match-workbook",
        str(match_workbook),
        "--match-side",
        match_side,
        str(input_doc),
        "-o",
        str(output_path),
    ]
    print("+ " + " ".join(quote_arg(part) for part in command))
    subprocess.run(command, cwd=ROOT_DIR, check=True)


def quote_arg(value: str) -> str:
    if not value or any(ch.isspace() for ch in value):
        return f'"{value}"'
    return value


def main(argv: list[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    date = choose_date(args)

    podm_doc = choose_path(
        args.podm_doc,
        "PODM_DOC",
        ROOT_DIR / "data" / date / PODM_DOC_NAME,
    )
    bmc_doc = choose_path(
        args.bmc_doc,
        "BMC_DOC",
        ROOT_DIR / "data" / date / BMC_DOC_NAME,
    )
    match_workbook = choose_path(
        args.match_workbook,
        "MATCH_WORKBOOK",
        ROOT_DIR / "output" / date / "analysis" / "interface_match_llm_summary.xlsx",
    )
    out_dir = choose_path(args.out_dir, "OUT_DIR", ROOT_DIR / "output" / date)

    require_files([EXTRACTOR, podm_doc, bmc_doc, match_workbook])
    out_dir.mkdir(parents=True, exist_ok=True)

    run_extractor(
        profile="bmc",
        match_side="bmc",
        input_doc=bmc_doc,
        match_workbook=match_workbook,
        output_path=out_dir / "bmc.common.word.interface-params.yaml",
    )
    run_extractor(
        profile="podm",
        match_side="podm",
        input_doc=podm_doc,
        match_workbook=match_workbook,
        output_path=out_dir / "podm.common.word.interface-params.yaml",
    )


if __name__ == "__main__":
    main()
