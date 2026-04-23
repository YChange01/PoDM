# 12 条示例路径漏抓的分类归因

> 数据源：`analysis/why_missing_report.txt`（修复前基线，2025-04-23 基于
> Atlas PoDManager 1.0.0 Redfish 接口参考文档）
>
> 全部 12 条漏抓，**根因单一**：都是文档作者"请求示例"块里 HTTP 首行
> 的排版手滑，`extract_from_examples.py` 的正则匹配不上。按具体 bug
> 形态分成三类。

## 类 A：Method 与 URI 无空格粘连（8 条）

| 章节 | 原文 HTTP 行 | 问题 |
|---|---|---|
| 4.2.64 | `PATCH/redfish/v1/...` | `PATCH` 后缺空格 |
| 4.2.70 | `POST/redfish/v1/...` | 同 |
| 4.2.71 | `POST/redfish/v1/...` | 同（而且 URI 抄的是 4.2.70 的，独立 bug） |
| 4.2.73 / 4.2.82 / 4.2.83 / 4.2.84 | `POST/redfish/v1/...` | 同 |

旧正则要求 `METHOD \s+ URI`，`POST/redfish` 中间没空格就失配。

## 类 B：URI 段中夹空格（3 条）

| 章节 | URI 写法 | 问题点 |
|---|---|---|
| 4.3.24 | `.../NetworkBridge/{bridge _id}` | 占位符里夹了个空格 |
| 4.3.62 | `.../Storage. ImportForeignConfig` | 点号后多一个空格 |
| 4.5.5 | `.../Oem/Huawei/ UpdateService.StartActivate` | 斜杠后多一个空格 |

旧正则的 `(\S+)` 一遇到空格就结束，剩余部分里找不到 `HTTP/...` 就失配。

## 类 C：URI 与 `HTTP/1.1` 粘连 + 请求行根本不存在（2 条）

| 章节 | 原文 | 问题 |
|---|---|---|
| 4.2.32 | `.Manager.PoDImportConfigurationHTTP/1.1` | URI 末尾没空格，直接黏上 `HTTP/1.1` |
| 4.10.4.2 | 只有 "Redfish会话请求头：" + headers，**没写**方法和 URI 那行 | 文档作者完全没写 HTTP 首行 |

4.10.4.2 是真遗漏（需要作者补），其他 11 条都是字符级手滑。

## 修法

`extract_from_examples.py` 正则放宽（方案 B）：

```python
# 旧
_HTTP_FIRST_RE = re.compile(r"(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s+HTTP/\S+")
# 新
_HTTP_FIRST_RE = re.compile(r"(GET|POST|PUT|PATCH|DELETE)\s*(\S.*?)\s*HTTP/\S+")
```

两处 `\s*` 允许 0 空格（覆盖类 A 和类 C），URI 段用 lazy `.*?` 代替 `\S+`
（覆盖类 B）。

**有意不做归一化**：抓到的 URI 原样带着文档原 bug（比如 `{bridge _id}`
里的空格、`Oem/Huawei/ UpdateService` 里的空格）。这样 `diff_uris.py`
后续能在表格 URI 和示例 URI 的差异报告里把这几条用 `SPACE_IN_URI`
/ `PATH_DIFF` 标签指出来，继续推文档作者去修 doc。

## 修复后结果

- 漏抓：12 → **1**（只剩 4.10.4.2，文档真遗漏，不是解析问题）
- 抓回的 11 条里，3 条（4.3.24/4.3.62/4.5.5）URI 里仍带着文档原 bug，
  继续在 `diff_uris.py` 的差异报告里暴露
