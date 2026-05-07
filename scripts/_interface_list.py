"""Interface-list YAML output shared by PoDManager and BMC extractors."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InterfaceSummary:
    section: str
    title: str
    method: str
    uri: str


def first_non_empty(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return ""


def dedup_prefer_uri(items: list[InterfaceSummary]) -> list[InterfaceSummary]:
    """按 (section, title) 去重：带 URI 的优先；否则保留较后出现的一条。"""
    best: dict[tuple[str, str], int] = {}
    for idx, item in enumerate(items):
        key = (item.section, item.title)
        prev = best.get(key)
        if prev is None:
            best[key] = idx
            continue
        prev_has_uri = bool(items[prev].uri)
        cur_has_uri = bool(item.uri)
        if cur_has_uri and not prev_has_uri:
            best[key] = idx
        elif cur_has_uri == prev_has_uri:
            best[key] = idx
    keep = set(best.values())
    return [item for idx, item in enumerate(items) if idx in keep]


def _yaml_scalar(value: str) -> str:
    """Format a scalar for readable YAML without requiring PyYAML."""
    if value == "":
        return "''"
    needs_quote = (
        value.strip() != value
        or "\n" in value
        or ": " in value
        or " #" in value
        or value[0] in "-?:,[]{}#&*!|>'\"%@`"
        or any(ch in value for ch in ("[", "]", "{", "}", ","))
    )
    if not needs_quote:
        return value
    return json.dumps(value, ensure_ascii=False)


def format_interface_list_yaml(items: list[InterfaceSummary]) -> str:
    if not items:
        return "interfaces: []\n"

    lines = ["interfaces:"]
    for index, item in enumerate(items, start=1):
        lines.append(f"- index: {index}")
        lines.append(f"  section: {_yaml_scalar(item.section)}")
        lines.append(f"  title: {_yaml_scalar(item.title)}")
        lines.append(f"  method: {_yaml_scalar(item.method)}")
        lines.append(f"  uri: {_yaml_scalar(item.uri)}")
    return "\n".join(lines) + "\n"


def write_interface_list_yaml(items: list[InterfaceSummary], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(format_interface_list_yaml(items), encoding="utf-8")
