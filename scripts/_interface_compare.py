"""Shared helpers for interface-list baseline comparisons."""
from __future__ import annotations

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InterfaceItem:
    section: str
    title: str
    method: str
    uri: str
    index: int = 0


def clean(value: object) -> str:
    return "" if value is None else str(value).strip()


def normalize_uri(uri: object) -> str:
    text = clean(uri)
    text = text.replace("新URL：", "")
    text = re.sub(r"^(GET|POST|PATCH|DELETE|PUT)\s+", "", text, flags=re.I)
    text = re.sub(r"^https?://[^/]+", "", text)
    text = text.replace(" ", "")
    text = text.replace("/Oem/Huawei/Public/", "/Oem/HuaweiPublic/")
    text = text.replace("/Oem/Huawei/Public", "/Oem/HuaweiPublic")
    text = text.replace("/Oem/Public/Huawei/", "/Oem/HuaweiPublic/")
    text = text.replace("/Oem/Huawei/", "/Oem/HuaweiPublic/")

    normalized_segments: list[str] = []
    for segment in text.split("/"):
        if not segment:
            continue
        if "?" in segment:
            base, query = segment.split("?", 1)
            query = re.sub(r"=[^&]+", "={id}", query)
            normalized_segments.append(f"{base}?{query}")
            continue
        if re.fullmatch(r"\{[^{}]+\}", segment):
            normalized_segments.append("{id}")
            continue
        if re.fullmatch(r"(?i)([a-z]+_)*[a-z]*id", segment):
            normalized_segments.append("{id}")
            continue
        normalized_segments.append(segment)
    return "/" + "/".join(normalized_segments)


def exact_key(item: InterfaceItem) -> tuple[str, str, str]:
    return (item.title, item.method.upper(), normalize_uri(item.uri))


def uri_key(item: InterfaceItem) -> tuple[str, str]:
    return (item.method.upper(), normalize_uri(item.uri))


def section_key(item: InterfaceItem) -> str:
    return item.section


def title_method_key(item: InterfaceItem) -> tuple[str, str]:
    return (item.title, item.method.upper())


def load_yaml_items(path: Path) -> list[InterfaceItem]:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - dependency is present in tests.
        raise SystemExit("读取 YAML 需要 PyYAML：python -m pip install pyyaml") from exc

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_items = data.get("interfaces") or []
    items: list[InterfaceItem] = []
    for raw in raw_items:
        items.append(
            InterfaceItem(
                section=clean(raw.get("section")),
                title=clean(raw.get("title")),
                method=clean(raw.get("method")),
                uri=clean(raw.get("uri")),
                index=int(raw.get("index") or len(items) + 1),
            )
        )
    return items


def item_from_row(row: dict[str, object], prefix: str = "") -> InterfaceItem:
    return InterfaceItem(
        section=clean(row.get(f"{prefix}section")),
        title=clean(row.get(f"{prefix}title")),
        method=clean(row.get(f"{prefix}method")),
        uri=clean(row.get(f"{prefix}uri")),
    )


def row_dicts(sheet) -> list[dict[str, object]]:
    headers = [cell.value for cell in next(sheet.iter_rows(min_row=1, max_row=1))]
    rows: list[dict[str, object]] = []
    for values in sheet.iter_rows(min_row=2, values_only=True):
        rows.append({header: values[index] if index < len(values) else None for index, header in enumerate(headers)})
    return rows


def pop_from_group(
    groups: dict[object, deque[int]],
    key: object,
    available: set[int],
) -> int | None:
    queue = groups.get(key)
    while queue and queue[0] not in available:
        queue.popleft()
    if queue:
        found = queue.popleft()
        available.remove(found)
        return found
    return None


def unique_group_match(
    groups: dict[object, list[int]],
    key: object,
    available: set[int],
) -> int | None:
    candidates = [idx for idx in groups.get(key, []) if idx in available]
    if len(candidates) == 1:
        available.remove(candidates[0])
        return candidates[0]
    return None


def build_match_indexes(items: list[InterfaceItem]) -> dict[str, object]:
    exact: dict[object, deque[int]] = defaultdict(deque)
    uri: dict[object, list[int]] = defaultdict(list)
    section: dict[object, list[int]] = defaultdict(list)
    title_method: dict[object, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        exact[exact_key(item)].append(index)
        uri[uri_key(item)].append(index)
        section[section_key(item)].append(index)
        title_method[title_method_key(item)].append(index)
    return {
        "exact": exact,
        "uri": uri,
        "section": section,
        "title_method": title_method,
    }


def match_baseline_item(
    baseline: InterfaceItem,
    new_items: list[InterfaceItem],
    indexes: dict[str, object],
    available: set[int],
) -> InterfaceItem | None:
    exact_groups = indexes["exact"]
    if isinstance(exact_groups, dict):
        idx = pop_from_group(exact_groups, exact_key(baseline), available)
        if idx is not None:
            return new_items[idx]

    for name, key in (
        ("uri", uri_key(baseline)),
        ("section", section_key(baseline)),
        ("title_method", title_method_key(baseline)),
    ):
        groups = indexes[name]
        if isinstance(groups, dict):
            idx = unique_group_match(groups, key, available)
            if idx is not None:
                return new_items[idx]
    return None


def field_change_note(side: str, baseline: InterfaceItem, current: InterfaceItem | None) -> str:
    if current is None:
        return f"{side}缺失"
    changes: list[str] = []
    if baseline.section != current.section:
        changes.append(f"section {baseline.section}->{current.section}")
    if baseline.title != current.title:
        changes.append(f"标题《{baseline.title}》->《{current.title}》")
    if baseline.method.upper() != current.method.upper():
        changes.append(f"method {baseline.method}->{current.method}")
    if normalize_uri(baseline.uri) != normalize_uri(current.uri):
        changes.append(f"URI {baseline.uri}->{current.uri}")
    elif baseline.uri != current.uri:
        changes.append(f"URI文本 {baseline.uri}->{current.uri}")
    if not changes:
        return ""
    prefix = f"{side}：" if side else ""
    return prefix + "，".join(changes)


def combine_notes(*parts: object) -> str:
    notes = [clean(part) for part in parts if clean(part)]
    return "；".join(notes)


def exact_new_pairs(
    left_items: list[InterfaceItem],
    right_items: list[InterfaceItem],
    available_left: set[int],
    available_right: set[int],
) -> list[tuple[int, int]]:
    left_groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    right_groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index in available_left:
        left_groups[uri_key(left_items[index])].append(index)
    for index in available_right:
        right_groups[uri_key(right_items[index])].append(index)

    pairs: list[tuple[int, int]] = []
    for key, left_group in sorted(left_groups.items(), key=lambda item: min(item[1])):
        right_group = right_groups.get(key, [])
        if len(left_group) == 1 and len(right_group) == 1:
            left_index, right_index = left_group[0], right_group[0]
            available_left.remove(left_index)
            available_right.remove(right_index)
            pairs.append((left_index, right_index))
    return pairs
