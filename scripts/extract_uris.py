"""
从 extract_headings.py 生成的 headings.txt 里抽取接口 URI，
输出一份带 [METHOD] 前缀的 URI 列表（每行一个），文档顺序保留，不去重。

headings.txt 里形如：
        [POST] /redfish/v1/Managers/{manager_id}/LogServices/.../LogService.ExportLog
的行会被识别为接口 URI 行。输出直接保留 [METHOD] 前缀与原始 URI。

兼容文档拼写瑕疵：URI 缺前导 '/' 的情况（如 "redfish/v1/..."）也会被抓到。

用法：
    python3 extract_uris.py                                    # 使用默认输入
    python3 extract_uris.py <input.headings.txt> [output.txt]

    默认输入：<仓库根>/output/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.headings.txt
    默认输出：<仓库根>/output/<输入文件名去掉.headings>.uris.txt

依赖：仅 Python 3 标准库。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = (
    REPO_ROOT / "output" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.headings.txt"
)
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"

# 缩进 + 整段保留（可选的 [METHOD] + 以 / 或 redfish 开头的 URI）。
# 用 (?:/|redfish) 兼容缺前导 / 的文档瑕疵。
_URI_LINE = re.compile(r"^\s+((?:\[[A-Z]+\]\s+)?(?:/|redfish)\S.*)$")


def extract_uris(text: str) -> list[str]:
    uris: list[str] = []
    for line in text.splitlines():
        m = _URI_LINE.match(line)
        if m:
            uris.append(m.group(1).rstrip())
    return uris


def _default_output_for(inp: Path) -> Path:
    name = inp.name
    if name.endswith(".headings.txt"):
        name = name[: -len(".headings.txt")] + ".uris.txt"
    else:
        name = inp.stem + ".uris.txt"
    return inp.parent / name


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        inp = Path(argv[1])
        out = Path(argv[2]) if len(argv) > 2 else _default_output_for(inp)
    else:
        inp = DEFAULT_INPUT
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = DEFAULT_OUTPUT_DIR / _default_output_for(inp).name
    return inp, out


def main() -> None:
    inp, out = _resolve_io(sys.argv)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")
    text = inp.read_text(encoding="utf-8")
    uris = extract_uris(text)
    out.write_text("\n".join(uris) + ("\n" if uris else ""), encoding="utf-8")
    print(f"已提取 {len(uris)} 个 URI -> {out}")


if __name__ == "__main__":
    main()
