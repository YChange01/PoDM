"""提取结果的数据类与文件输出。两个 extractor 共用。

分离原因：之前 Params/Interface dataclass 和 dump_yaml 在两个 extractor
里各写一遍，已经发生过样式漂移（一边用 SafeDumper、一边用 add_representer
顺序不同等小差异）。统一到这里防止再分叉。
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


# =================== 数据类 ===================

@dataclass
class Params:
    path: list[str] = field(default_factory=list)
    header: list[str] = field(default_factory=list)
    body: list[str] = field(default_factory=list)
    query: list[str] = field(default_factory=list)
    response: list[str] = field(default_factory=list)


@dataclass
class Interface:
    section: str
    title: str
    method: str
    uri: str
    params: Params


# =================== 通用工具 ===================

def dedup_keep_order(items: list[str]) -> list[str]:
    """保序去重。"""
    seen: set[str] = set()
    out: list[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


# =================== 文件输出 ===================

def dump_yaml(data: dict, out: Path) -> Path:
    """把 data 写成 YAML（PyYAML 不在则降级到 JSON，路径自动改后缀）。"""
    try:
        import yaml
    except ImportError:
        print(
            "提示：未安装 PyYAML，自动改输出 JSON。`pip install pyyaml` 可切回 YAML。",
            file=sys.stderr,
        )
        out = out.with_suffix(".json")
        out.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return out

    def _str_repr(dumper, value):
        if "\n" in value:
            return dumper.represent_scalar("tag:yaml.org,2002:str", value, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", value)

    yaml.add_representer(str, _str_repr, Dumper=yaml.SafeDumper)
    out.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    return out


def write_uris(interfaces: list[Interface], out: Path) -> None:
    """interfaces 的 method+uri 写成每行 "[METHOD] URI" 的 txt。"""
    lines: list[str] = []
    for iface in interfaces:
        if iface.method:
            lines.append(f"[{iface.method}] {iface.uri}")
        else:
            lines.append(iface.uri)
    out.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )


def write_warnings(warnings: list[str], out: Path) -> Path | None:
    """warning 列表 → utf-8 文件。空列表返回 None（不创建文件）。

    每条 warning 一行，调用方负责格式化（建议格式：
    "<section> <title> <reason>"）。
    """
    if not warnings:
        return None
    out.write_text("\n".join(warnings) + "\n", encoding="utf-8")
    return out
