#!/usr/bin/env python3
"""Run the full extraction pipeline into output/<date>/."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))
from _defaults import BMC_DOCX_NAME, DATA_DIR, OUTPUT_DIR, PODM_DOCX_NAME  # noqa: E402

DATE_RE = re.compile(r"^\d{8}$")


def validate_date(date: str) -> str:
    if not DATE_RE.match(date):
        raise SystemExit(f"日期必须是 YYYYMMDD 格式: {date}")
    return date


def default_inputs_for_date(date: str) -> tuple[Path, Path]:
    data_dir = DATA_DIR / date
    return data_dir / PODM_DOCX_NAME, data_dir / BMC_DOCX_NAME


def output_paths(out_dir: Path, podm: Path, bmc: Path) -> dict[str, Path]:
    return {
        "podm_interface_list": out_dir / f"{podm.stem}.interface-list.yaml",
        "bmc_interface_list": out_dir / f"{bmc.stem}.interface-list.yaml",
        "podm_tables": out_dir / f"{podm.stem}.interfaces.yaml",
        "podm_examples": out_dir / f"{podm.stem}.example.interfaces.yaml",
        "bmc_params": out_dir / f"{bmc.stem}.bmc.interfaces.yaml",
    }


def run_command(args: list[str]) -> None:
    print("+ " + " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def run_pipeline(
    date: str,
    output_root: Path,
    podm: Path | None = None,
    bmc: Path | None = None,
) -> Path:
    run_date = validate_date(date)
    default_podm, default_bmc = default_inputs_for_date(run_date)
    podm = (podm or default_podm).resolve()
    bmc = (bmc or default_bmc).resolve()
    missing = [str(path) for path in (podm, bmc) if not path.exists()]
    if missing:
        raise SystemExit("输入文件不存在:\n  " + "\n  ".join(missing))

    out_dir = output_root.resolve() / run_date
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = output_paths(out_dir, podm, bmc)

    run_command([
        sys.executable,
        str(SCRIPTS / "extract_podm_interface_list.py"),
        str(podm),
        str(paths["podm_interface_list"]),
    ])
    run_command([
        sys.executable,
        str(SCRIPTS / "extract_bmc_interface_list.py"),
        str(bmc),
        str(paths["bmc_interface_list"]),
    ])
    run_command([
        sys.executable,
        str(SCRIPTS / "extract_from_tables.py"),
        str(podm),
        str(paths["podm_tables"]),
    ])
    run_command([
        sys.executable,
        str(SCRIPTS / "extract_from_examples.py"),
        str(podm),
        str(paths["podm_examples"]),
    ])
    run_command([
        sys.executable,
        str(SCRIPTS / "extract_bmc.py"),
        str(bmc),
        str(paths["bmc_params"]),
    ])

    print(f"流水线完成 -> {out_dir}")
    return out_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="一键提取 PoDManager/BMC 接口清单和接口+参数，输出到 output/<date>/"
    )
    parser.add_argument("date", help="日期目录，例如 20260507")
    parser.add_argument("--podm", type=Path, help="PoDManager 文档路径；默认 data/<date>/固定文件名")
    parser.add_argument("--bmc", type=Path, help="BMC 文档路径；默认 data/<date>/固定文件名")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR, help="输出根目录")
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args(sys.argv[1:])
    run_pipeline(args.date, args.output_root, args.podm, args.bmc)


if __name__ == "__main__":
    main()
