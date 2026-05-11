#!/usr/bin/env python3
"""Extract BMC and PoDManager interface lists for LLM matching.

This script is the first step in the manual LLM-assisted workflow. It extracts
only interface metadata (`index/section/title/method/uri`) from the two Word
documents, then writes a copy-friendly Markdown input file for the common/unique
interface review step.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _defaults import BMC_DOCX_NAME, PODM_DOCX_NAME  # noqa: E402


DEFAULT_DATE = "20260507"
DATE_RE = re.compile(r"^\d{8}$")

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="提取 BMC/PoDM 接口清单，并生成用于大模型判断共有/独有接口的复制文件"
    )
    parser.add_argument(
        "date_arg",
        nargs="?",
        help=f"日期目录，例如 20260507；默认 {DEFAULT_DATE}",
    )
    parser.add_argument("--date", dest="date_opt", help="日期目录，例如 20260507")
    parser.add_argument("--podm-doc", type=Path, help="PoDManager Word 文档路径")
    parser.add_argument("--bmc-doc", type=Path, help="BMC Word 文档路径")
    parser.add_argument("--out-dir", type=Path, help="输出目录；默认 output/<date>")
    parser.add_argument(
        "--copy-input",
        type=Path,
        help="复制给大模型的 Markdown 文件；默认 output/<date>/analysis/interface_match_llm_input.md",
    )
    return parser.parse_args(argv)


def choose_date(args: argparse.Namespace) -> str:
    date = args.date_opt or args.date_arg or DEFAULT_DATE
    if not DATE_RE.match(date):
        raise SystemExit(f"日期必须是 YYYYMMDD 格式: {date}")
    return date


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


def run_command(args: list[str]) -> None:
    print("+ " + " ".join(quote_arg(part) for part in args))
    subprocess.run(args, cwd=ROOT_DIR, check=True)


def quote_arg(value: str) -> str:
    if not value or any(ch.isspace() for ch in value):
        return f'"{value}"'
    return value


def write_interface_match_input(
    bmc_list: Path,
    podm_list: Path,
    output: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    bmc_yaml = bmc_list.read_text(encoding="utf-8")
    podm_yaml = podm_list.read_text(encoding="utf-8")
    output.write_text(
        "\n".join(
            [
                "# BMC vs PoDManager Redfish 接口匹配输入",
                "",
                "请基于下面两份 interface-list YAML 判断共有接口、BMC 独有接口、PoDM 独有接口。",
                "要求：",
                "",
                "- 按 method、URI、URI skeleton、Action 名称和接口语义判断，不只看标题。",
                "- 共有接口必须一对一匹配。",
                "- 输出一个 Excel 工作簿：`interface_match_llm_summary.xlsx`。",
                "- 工作簿必须包含且仅包含三个 sheet：`共有接口`、`BMC独有`、`PoDM独有`。",
                "- `共有接口` 建议列：`category, confidence, title_similarity_score, method_same, bmc_index, bmc_section, bmc_title, bmc_method, bmc_uri, podm_index, podm_section, podm_title, podm_method, podm_uri`。",
                "",
                "## BMC interface-list.yaml",
                "",
                "```yaml",
                bmc_yaml.rstrip(),
                "```",
                "",
                "## PoDManager interface-list.yaml",
                "",
                "```yaml",
                podm_yaml.rstrip(),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    date = choose_date(args)
    data_dir = ROOT_DIR / "data" / date
    out_dir = choose_path(args.out_dir, "OUT_DIR", ROOT_DIR / "output" / date)

    podm_doc = choose_path(args.podm_doc, "PODM_DOC", data_dir / PODM_DOCX_NAME)
    bmc_doc = choose_path(args.bmc_doc, "BMC_DOC", data_dir / BMC_DOCX_NAME)
    copy_input = args.copy_input or out_dir / "analysis" / "interface_match_llm_input.md"

    require_files([podm_doc, bmc_doc])
    out_dir.mkdir(parents=True, exist_ok=True)

    podm_list = out_dir / f"{podm_doc.stem}.interface-list.yaml"
    bmc_list = out_dir / f"{bmc_doc.stem}.interface-list.yaml"

    run_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "extract_podm_interface_list.py"),
            str(podm_doc),
            str(podm_list),
        ]
    )
    run_command(
        [
            sys.executable,
            str(SCRIPT_DIR / "extract_bmc_interface_list.py"),
            str(bmc_doc),
            str(bmc_list),
        ]
    )
    write_interface_match_input(bmc_list, podm_list, copy_input)

    print(f"接口清单已生成:\n  {bmc_list}\n  {podm_list}")
    print(f"复制给大模型的输入文件:\n  {copy_input}")


if __name__ == "__main__":
    main()
