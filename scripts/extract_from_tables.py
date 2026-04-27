#!/usr/bin/env python3
"""
从 PoDManager 接口文档 (.docx 或 .txt) 中逐个接口提取 URI 与参数名。

每个接口只抽取"表格第一列"的参数名（即参数名称），按 path/header/body/query/response 分类：

    interfaces:
      - section: "4.2.25"
        title:   "导出日志信息"
        method:  POST
        uri:     /redfish/v1/Managers/{manager_id}/...
        params:
          path:     [manager_id, logservices_id]
          header:   [X-Auth-Token, Content-Type]
          body:     [Type, Content]
          query:    []
          response: ["@odata.context", "@odata.type", ...]

用法：
    python3 extract_from_tables.py                             # 使用默认输入
    python3 extract_from_tables.py <输入文件> [输出yaml]

    默认输入：<仓库根>/data/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx
    默认输出（output/）：
      - <stem>.interfaces.yaml         结构化
      - <stem>.uris.txt                每行 "[METHOD] URI"，顺序与 yaml 一致
      - <stem>.tables.warnings.txt     extractor 跳过/异常的 section（仅有时才创建）

依赖：仅 Python 3 标准库；若安装了 PyYAML 则用 YAML 输出，否则自动回退 JSON。

模块组织：
    - 文档结构识别（章节/marker/表标题/iter_tables）→ _doc_structure
    - 数据类与文件输出（Params/Interface/dump_yaml）→ _yaml_io
    - 本文件保留：表格"参数名称首列"识别（type 列启发式 + 名称正则）
"""
from __future__ import annotations

import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _docx_utils import read_source  # noqa: E402
from _doc_structure import (  # noqa: E402  (部分名字也对外 re-export 给 col_enum/type_enum/why_missing)
    dedup_sections,
    iter_tables,
    section_has_uri,
    split_columns,
    split_sections,
    split_subsections,
)
from _yaml_io import (  # noqa: E402
    Interface,
    Params,
    dump_yaml,
    write_uris,
    write_warnings,
)

# ---- 向后兼容别名：旧调用方按下划线私名导入 ----
_section_has_uri = section_has_uri


# =================== 表格"参数名称"首列识别 ===================

REQUIRED_VALUES = {"是", "否", "必选", "可选"}
# 白名单由 scripts/type_enum.py 扫描全文档"类型"列的真实取值，按出现次数 ≥2 的
# 合法类型词归入而成。
TYPE_VALUES = {
    # --- 英文 ---
    "string", "int", "integer", "uint", "bool", "boolean", "array", "object",
    "float", "number", "null", "list", "dict", "enum", "long", "short",
    "double", "map", "byte", "timestamp",
    "String",  # 大写首字母变体
    "URI",     # Redfish 把 URI 当类型用
    "array[object]", "array[string]",  # 带方括号的数组语法
    # --- 中文基础类型 ---
    "字符串", "字符", "字符型",
    "数字", "整数", "整型", "长整型", "短整型",
    "布尔", "布尔值", "布尔型",
    "浮点", "浮点数", "浮点型", "小数",
    "枚举", "枚举型",
    "数组", "列表", "对象", "字典", "集合", "映射",
    "自定义属性", "属性",
    "日期", "时间", "时间戳", "字节",
    # --- 文档里把类名当类型用的情况 ---
    "用户", "角色", "权限", "权限集合",
    # --- 联合/特殊写法 ---
    "null或字符串",
    # --- "-" 与 en-dash "–"：类型列留空用 "-" 占位（真实文档 350+43 次）---
    "-", "–",
}
# "整型/字符型/浮点型" 等以 型 结尾的变体统一兜底；
# "xx列表/xx数组/xx对象/xx集合/xx属性/xx字典/xx映射" 类 domain-specific 类型也归这里
TYPE_SUFFIX_RE = re.compile(r"^.{0,10}(列表|数组|对象|集合|属性|字典|映射|型)$")
# 参数名长相：ASCII 字母/@/_ 开头，只含 ASCII 字母数字和 _ @ . - /
# 用于两个地方：①过滤非标识符首列（避免"文件传输协议包括：sftp"被 "-" 触发成新行）
#              ②结构补救：上一行刚结束、首列像参数名、整行 ≥2 列 时也视为新行
_NAME_LIKE_RE = re.compile(r"^[@A-Za-z_][A-Za-z0-9_@./\-]*$")


def looks_like_type(s: str) -> bool:
    if not s:
        return False
    if s in REQUIRED_VALUES or s in TYPE_VALUES:
        return True
    return bool(TYPE_SUFFIX_RE.match(s))


def is_new_row(cols: list[str]) -> bool:
    """新行的第 2~3 列应当是"是/否"或类型词。"""
    if len(cols) < 2:
        return False
    for i in range(1, min(4, len(cols))):
        if looks_like_type(cols[i]):
            return True
    return False


def extract_param_names(body_lines: list[str]) -> list[str]:
    """从一个表的正文里抽取"参数名称"（每个新行的第一列）。

    不做去重：同名重复通常代表嵌套字段（如 Members 下的 @odata.id），丢弃会丢信息。

    两条新行判定规则：
      ① 类型命中（白名单/后缀）——is_new_row
      ② 结构补救——上一行没有续行过 & 首列是标识符 & ≥2 列
         覆盖类型列漏填的行，如 "NameServers  指定网口地址为动态模式时，所需的DNS服务器信息。"
    """
    names: list[str] = []
    iter_lines = iter(body_lines)
    # 跳过表头（第一个非空行）
    for line in iter_lines:
        if line.strip():
            break

    in_row = False          # 是否有"当前行"
    cont_count = 0          # 当前行已吃到的续行数量
    for line in iter_lines:
        if not line.strip():
            continue
        cols = split_columns(line)
        if not cols:
            continue

        type_hit = is_new_row(cols)
        struct_hit = (
            not type_hit
            and in_row
            and cont_count == 0
            and len(cols) >= 2
            and bool(_NAME_LIKE_RE.match(cols[0]))
        )

        if type_hit or struct_hit:
            # 过滤首列不是参数名长相的行——如 "文件传输协议包括：sftp" 这种中文描述
            # 被 col[1]='-' 触发 type_hit=True，但首列不像参数名，忽略它
            if _NAME_LIKE_RE.match(cols[0]):
                names.append(cols[0])
            in_row = True
            cont_count = 0
        else:
            if in_row:
                cont_count += 1
    return names


def classify_table(title: str) -> str:
    lower = title.lower()
    if "path" in lower:
        return "path"
    if "header" in lower:
        return "header"
    if "body" in lower:
        return "body"
    if "query" in lower:
        return "query"
    if "response" in lower or "响应" in title or "返回" in title:
        return "response"
    return "other"


# =================== 组装接口 ===================

def first_non_empty(lines: list[str]) -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return ""


def build_interface(section: dict) -> Interface:
    subs = split_subsections(section["lines"])
    params = Params()

    for title, body_lines in iter_tables(subs["请求参数"]):
        names = extract_param_names(body_lines)
        category = classify_table(title)
        if category in ("path", "header", "body", "query"):
            getattr(params, category).extend(names)

    for _, body_lines in iter_tables(subs["响应参数"]):
        params.response.extend(extract_param_names(body_lines))

    return Interface(
        section=section["number"],
        title=section["title"],
        method=first_non_empty(subs["调用方法"]),
        uri=first_non_empty(subs["URI"]),
        params=params,
    )


# =================== 入口 ===================

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "data" / "Atlas PoDManager 1.0.0 Redfish 接口参考_最新.docx"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output"


def _resolve_io(argv: list[str]) -> tuple[Path, Path]:
    if len(argv) >= 2:
        inp = Path(argv[1])
        out = (
            Path(argv[2])
            if len(argv) > 2
            else inp.with_suffix(".interfaces.yaml")
        )
    else:
        inp = DEFAULT_INPUT
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out = DEFAULT_OUTPUT_DIR / f"{inp.stem}.interfaces.yaml"
    return inp, out


def main() -> None:
    inp, out = _resolve_io(sys.argv)
    if not inp.exists():
        sys.exit(f"输入文件不存在: {inp}")

    text = read_source(inp)
    all_sections = split_sections(text)
    sections = dedup_sections(all_sections)
    dropped = len(all_sections) - len(sections)

    warnings: list[str] = []
    interfaces: list[Interface] = []
    for sec in sections:
        if not section_has_uri(sec):
            continue
        try:
            iface = build_interface(sec)
        except Exception as exc:  # pragma: no cover
            warnings.append(f"{sec['number']}\t{sec['title']}\t解析异常: {exc}")
            continue
        if not iface.uri:
            warnings.append(f"{sec['number']}\t{sec['title']}\tURI 子段为空，已跳过")
            continue
        if not iface.method:
            warnings.append(f"{sec['number']}\t{sec['title']}\t调用方法 子段为空")
        interfaces.append(iface)

    data = {"interfaces": [asdict(i) for i in interfaces]}
    final_yaml = dump_yaml(data, out)

    # <stem>.interfaces.yaml → 取最里层 stem 当 base
    base_stem = Path(out.stem).stem if "." in out.stem else out.stem
    uris_path = out.parent / f"{base_stem}.uris.txt"
    warn_path = out.parent / f"{base_stem}.tables.warnings.txt"

    write_uris(interfaces, uris_path)
    written_warn = write_warnings(warnings, warn_path)

    dup_note = f"，去重 {dropped} 条章节" if dropped else ""
    print(f"已提取 {len(interfaces)} 个接口{dup_note}")
    print(f"  YAML:  {final_yaml}")
    print(f"  URIs:  {uris_path}")
    if written_warn:
        print(f"  WARN:  {written_warn} ({len(warnings)} 条)")


if __name__ == "__main__":
    main()
