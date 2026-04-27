# PoDManager Redfish 接口文档 doc bug 总清单

## 数据源

| 文件 | 说明 |
|---|---|
| `output/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.interfaces.yaml` | 表格抓取，371 条接口 |
| `output/Atlas PoDManager 1.0.0 Redfish 接口参考_最新.example.interfaces.yaml` | 示例抓取，370 条接口 |
| `output/uri_diff.txt` | URI / method 对比，56 条 URI 不一致 + 5 条仅 method 不同 |
| `output/param_diff.txt` | 参数集合对比 |

## 类型概览

| 类型 | 数量 | 严重度 | 备注 |
|---|---:|---|---|
| A. URI 形式错误 | 49 | 高 | 客户端按 doc 直接拼错 URL |
| B. 参数名拼写 / 空格 | 15+ | 高 | 客户端按 doc 找不到字段 |
| C. Action 前缀写法不统一 | 60+ | 中 | 系统性约定问题 |
| D. 文档结构 / Marker 不规范 | 5 | 中 | 解析工具会误抓或漏抓 |
| E. JSON 示例语法错 | 3+ | 中 | JSON 不能直接 parse |
| F. 响应表与响应示例字段差异 | 280+ | 低-中 | schema vs 实例的常态差，需逐条评审 |

---

## 类型 A — URI 形式错误

### A1. URI 缺前导 `/`（5 条，全在 examples 侧）

| section | 标题 | 现 examples URI | 建议 |
|---|---|---|---|
| 4.2.76 | 查询当前告警信息 | `redfish/v1/Managers/{manager_id}/LogServices/EventLog/Oem/Huawei/HealthEvent/Entries` | 加前导 `/` |
| 4.2.77 | 查询系统日志集合资源信息 | `redfish/v1/Managers/{manager_id}/LogServices/EventLog/Entries` | 加前导 `/` |
| 4.2.78 | 查询系统日志资源信息 | `redfish/v1/Managers/{manager_id}/LogServices/EventLog/Entries/{entries_id}` | 加前导 `/` |
| 4.2.80 | 恢复刀片出厂设置 | `redfish/v1/Managers/{manager_id}/Actions/Manager.RestoreFactory` | 加前导 `/` |
| 4.2.81 | 恢复整框出厂设置 | `redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager.RestoreFactory` | 加前导 `/` |

> 另：表格侧 4.2.6、4.2.7（SnmpService.ConfigSnmpV3PrivPasswd / SubmitTestEvent）同样缺前导 `/`，建议表格段也补全。

### A2. URI 含多余的 `//`（8 条）

| section | 标题 | 出错处 | 建议 |
|---|---|---|---|
| 4.2.104 | 上载UBM文件 | `Managers//SMN1(SMN2)` | 删多余 `/`，并改用 `{manager_id}` 占位（见 A6） |
| 4.2.116 | 设置TPCM服务信息 | `//redfish/v1/...` | 删开头多余 `/` |
| 4.2.119 | 备份刀片配置文件 | `//redfish/v1/...Manager.BackupConfiguratione` | 删开头多余 `/`；同时拼写 → `BackupConfiguration`（A5） |
| 4.2.120 | 还原刀片配置文件 | `//redfish/v1/...Manager.RestoreConfiguratione` | 删开头多余 `/`；拼写 → `RestoreConfiguration` |
| 4.2.121 | 添加删除黑白名单命令的IPMI命令表 | `//redfish/v1/...` | 删开头多余 `/` |
| 4.4.30 | 查询服务器扩展板卡集合资源信息 | `Chassis/{chassis_id}//Boards` | 删 `Boards` 前多余 `/` |
| 4.4.31 | 查询指定扩展板卡资源信息 | `Chassis/{chassis_id}//Boards/{board_id}` | 同上 |
| 4.4.32 | 修改指定拓展板卡资源属性 | `Chassis/{chassis_id}//Boards/{board_id}` | 同上 |

### A3. URI 含空格（1 条）

| section | 标题 | 出错处 | 建议 |
|---|---|---|---|
| 4.5.5 | 生效固件 | `Oem/Huawei/ UpdateService.StartActivate` | 删 `Huawei/` 与 `UpdateService` 之间的空格 |

> 另：`{bridge _id}`（4.3.24）、`Storage. ImportForeignConfig`（4.3.62）表格 / 示例两侧都有空格，建议同步删除。

### A4. URI 截断 / 不完整（3 条，全在 examples 侧）

| section | 标题 | 现 examples URI | 建议 |
|---|---|---|---|
| 4.3.22 | 配置Bond | `/Actions/NetworkBonding.Configure` | 补完整 `/redfish/v1/Systems/{system_id}/NetworkBondings/{bond_id}/Actions/...` |
| 4.3.59 | 清空网口历史占用率资源信息 | `/Actions/Oem/Huawei/Public/ComputerSystem.ClearNetworkHistoryUsageRate` | 补完整 `/redfish/v1/Systems/{system_id}/...` 前缀 |
| 4.4.33 | NPU模组复位 | `/Boards/ACUBoard/Actions/NpuBoard.NpuBoardReset` | 补完整 `/redfish/v1/Chassis/{chassis_id}/Boards/...` 前缀 |

### A5. URI 拼写错（6 条，examples 侧）

| section | 标题 | 错误 | 应为 |
|---|---|---|---|
| 4.2.119 | 备份刀片配置文件 | `Manager.BackupConfiguratione` | `Manager.BackupConfiguration` |
| 4.2.120 | 还原刀片配置文件 | `Manager.RestoreConfiguratione` | `Manager.RestoreConfiguration` |
| 4.4.42 | 查询历史功率资源信息 | `Power.PowerHistoryDat` | `Power.PowerHistoryData` |
| 4.5.6 | 文件上传 | `UpdateService/FirmwareInventor` | `UpdateService/FirmwareInventory` |
| 4.10.6.5 | 导入南向SSL服务器证书 | `HttpsCert.ImportServerSouthCertificat` | `HttpsCert.ImportServerSouthCertificate` |
| 4.10.7.6 | 删除CA证书吊销列表 | `CertificateService.DeleteCACertificateCR` | `CertificateService.DeleteCACertificateCRL` |

### A6. URI 用具体值代替 `{占位符}`（28 条）

文档示例 URI 大量直接写实际值（`SMN1`、`Blade12-HDDPlaneDisk1` 等），导致客户端无法直接复用。建议**示例 URI 统一保持 `{xxx}` 占位符**，具体值放在请求示例正文里说明。

| section | tables（应为模板） | examples（被替换成实例） |
|---|---|---|
| 4.2.65 / 4.2.66 / 4.2.67 / 4.2.68 | `{manager_id}` | `SMN1` |
| 4.2.117 / 4.2.118 / 4.2.119 / 4.2.120 / 4.2.121 | `{manager_id}` | `SMN1` 或 `Blade13` |
| 4.4.3 | `{chassis_id}` | `SMN1` |
| 4.4.27 | `{drive_id}` | `HDDPlaneDisk1` |
| 4.4.29 | `{drive_id}` | `mainboardPCIeCard4(SSD)` |
| 4.4.56 / 4.4.57 | `Chassis/{chassis_id}/Sensors[/{sensor_id}]` | `Chassis/Sensors[/{sensor_id}]`（少一段 path）|
| 4.4.20 / 4.4.21 / 4.4.22 / 4.4.25 / 4.4.35 / 4.4.40 | 多个 `{xxx}` | 缺一层或多层占位符 |
| 4.9.7 / 4.9.8 / 4.9.9 | `MetricReportDefinitions/{id}` | `MetricReportDefinitions`（少 `/{id}`）|
| 4.2.57 | `SystemErase/{member_id}` | `SystemErase`（少 `/{member_id}`）|
| 4.4.18 | `PowerConverters/{powerconverter_id}` | `PowerConverters`（少占位符）|
| 4.3.36 | `Volumes/{volume_id}` | `Volumes`（少占位符）|
| 4.8.5 | `?ComponentType={component}&...` | `?ComponentType=CPU&...`（query 用具体值）|

### A7. URI 路径结构差异（15 条，需 doc 主核对）

| section | 标题 | 差异 |
|---|---|---|
| 4.2.2 / 4.2.3 | 查询/修改指定管理资源信息 | tables `{manager_id}` vs examples `{SMN(1\|2)}`——示例占位符写法不规范，应统一 `{manager_id}` |
| 4.2.52 / 4.2.53 / 4.2.54 | SP 服务硬盘擦除配置 | tables 路径 `SPService/SPDriveErase` vs examples 路径 `SPService/SPDiagnose/SPDriveErase`——**两条路径不一致，需确认实际 API 路径** |
| 4.2.71 | 删除截屏 | tables `DiagnosticService.DeleteScreenShot` vs examples `DiagnosticService.CaptureScreenShot`——**Action 名错位** |
| 4.2.102 / 4.2.105 | 启动纳管 / 上载文件 | URI 中 `SMN1(SMN2) /` 后多空格 |
| 4.3.28 | 查询VLAN集合资源信息 | tables `Systems/{system_id}/EthernetInterfaces/...` vs examples `Systems/{system_id}/Memory/{memory_id}/EthernetInterfaces/...`——**examples 多了一段错误路径** |
| 4.3.30 | 配置VLAN | tables 是 POST，examples 是 GET；URI 缺 `/` 隔开 `{vlan_id}` 和 `Actions` |
| 4.3.43 | 修改BIOS密码 | tables `Bios.ChangePassword` vs examples `Bios.ResetBios`——**Action 错位** |
| 4.4.42 | 查询历史功率资源信息 | URI 拼写 `Power.PowerHistoryDat` 缺 `a`（A5） |
| 4.5.6 | 文件上传 | URI 拼写 `FirmwareInventor` 缺 `y`（A5） |
| 4.6.1 | 查询任务服务资源信息 | tables `/redfish/v1/TaskService` vs examples `/redfish/v1/TaskService/Tasks/{taskid}`——examples 写错成单任务路径 |
| 4.9.11 | 查询指定指标报告资源信息 | examples 缺一段（A2 `//` 已含）|

### A8. URI method 不一致（6 条）

| section | 标题 | tables method | examples method | 建议 |
|---|---|---|---|---|
| 4.2.39 | 创建SP服务的OS安装配置 | GET | POST | 创建用 POST，**改 tables** |
| 4.2.69 | 导出录像 | POST | GET | 导出动作通常 POST，**改 examples** |
| 4.3.30 | 配置VLAN | POST | GET | "配置"动作用 POST，**改 examples** |
| 4.3.38 | 初始化指定逻辑盘 | POST | PATCH | "初始化"动作用 POST，**改 examples** |
| 4.4.9 | 查询指定机柜电源信息 | GET | POST | "查询"用 GET，**改 examples** |
| 4.10.2.12 | 查询南向SSL证书更新服务资源信息 | GET | PATCH | "查询"用 GET，**改 examples** |

---

## 类型 B — 参数名拼写 / 空格

### B1. 参数名前后含空格（4 处，examples 侧 JSON 实际写法）

| section | 类别 | 错误 | 应为 |
|---|---|---|---|
| 4.2.27 | response | `' Interface '` | `'Interface'` |
| 4.3.36 | response | `'StripSizeBytes '` | `'StripSizeBytes'` |
| 4.7.11 | body | `'Enabled '` | `'Enabled'` |
| 4.7.12 | body | `'Level '` | `'Level'` |

> 直接修示例 JSON 的字段名，删两侧空格。

### B2. 参数名 typo（11 处确定的）

| section | 类别 | 哪边错 | 错误 | 应为 |
|---|---|---|---|---|
| 4.2.4 | response | examples 多了一行 | `BobEnabled` | （疑似 `Enabled` 的笔误，需作者确认）|
| 4.2.20 | body | examples | `SubneMask` | `SubnetMask` |
| 4.2.22 | response | tables | `Lnks` | `Links` |
| 4.2.26 | response | tables | `Members@odata.nextLin` | `Members@odata.nextLink` |
| 4.2.35 | response | examples | `BaseVersioin` | `BaseVersion` |
| 4.2.39 | body | tables | `PackagaeName` | `PackageName` |
| 4.2.40 | response | tables | `MonitoringIntertval` | `MonitoringInterval` |
| 4.2.78 | response | tables | `EntryTyp` | `EntryType` |
| 4.3.19 | header | tables | `IsOnBoo` | `IsOnBoot` |
| 4.9.4 | response | tables | `MaxReaingRange` | `MaxReadingRange` |
| 4.10.5.2 / 4.10.6.2 | response | tables | `@odata.content` | `@odata.context` |

### B3. 大小写不一致（少量）

| section | 类别 | tables | examples | 建议 |
|---|---|---|---|---|
| 4.10.1.3 | response | `Error` / `Code` | `error` / `code` | 改 tables，统一用小写（与 Redfish 规范一致）|
| 4.10.4.3 / 4.10.4.5 | response | `oem` / `huawei` | `oem` / `huawei` | examples JSON 用小写，但 Redfish 规范应大写 `Oem` / `Huawei`，**改 examples**|
| 4.4.45 | response | `@Redfish.ActionInfo` | `@redfish.Actioninfo` | examples 大小写错，改 examples |

---

## 类型 C — Action / ActionInfo 前缀写法系统性不统一（60+ 处）

**现象**：tables 表里写不带前缀的 `Manager.Reset`、`Redfish.ActionInfo`，examples JSON 里则按 Redfish 规范写 `#Manager.Reset`、`@Redfish.ActionInfo`。

**示例（共发现于 ≥30 个接口）**：

| section | tables 写法 | examples 写法 |
|---|---|---|
| 4.2.2 | `Manager.Reset`、`Redfish.ActionInfo`、`Manager.GeneralDownload` ... | `#Manager.Reset`、`@Redfish.ActionInfo`、`#Manager.GeneralDownload` ... |
| 4.2.28 / 4.2.29 | `SyslogService.SubmitTestEvent` | `#SyslogService.SubmitTestEvent` |
| 4.4.6 | `Thermal.ClearInletHistoryTemperature` | `#Thermal.ClearInletHistoryTemperature` |
| 4.5.1 | `UpdateService.StartActivate` / `UpdateService.ParallelUpdate` | `#UpdateService.StartActivate` / `#UpdateService.ParallelUpdate` |
| 4.7.1 | `EventService.SubmitTestEvent` 等 6 个 | 全部 `#EventService.X` |
| 4.12.1 | `AssetService.ConfirmTrustedSupplyChain` | `#AssetService.ConfirmTrustedSupplyChain` |
| ... | （还有 50+ 接口同模式）| |

**建议**：tables 表里所有 Action 字段名补 `#` 前缀，所有 ActionInfo 字段名补 `@` 前缀，与 Redfish 规范一致。可批量替换。

---

## 类型 D — 文档结构 / Marker 写法不规范

### D1. 4.10.4.2 创建会话（登录）—— 请求示例缺 HTTP 首行

**现状**：请求示例段直接以 `Redfish会话请求头：` 开头，没有 `POST /redfish/v1/SessionService/Sessions HTTP/1.1` 首行。

**影响**：解析工具无法提取该接口的 method/uri/header/body，**整条接口被丢弃**（370 条 vs 371 条差就在这一条）。

**建议**：在请求示例段最前面补一行 HTTP 首行：
```
POST /redfish/v1/SessionService/Sessions HTTP/1.1
Host: 192.168.2.101
Content-Type: application/json
...
```

### D2. SMN板 / 业务板 等"X板XX参数"形式 marker

**现状**：4.4.2、4.4.3 在响应参数 / 响应示例段里出现 `SMN板响应参数`、`业务板响应参数`、`SMN板响应示例` 等带前缀的 marker。

**影响**：之前的解析工具完全识别不出，整段响应表 / 响应示例被丢失。已在 extractor 侧通过放宽正则修复。

**建议**：长期方案——文档统一改用 `响应参数 1` / `响应参数 2`（数字编号）+ 在表内首行加一行说明"适用机型：SMN板 / 业务板"，避免 marker 含业务语义。

### D3. "请求示例 1" / "响应参数 1" 数字前空格

**现状**：4.2.39 的 5 组示例（请求示例 1/2/3/4/6）和 4.4.27 的 4 组示例都用"X 1"（marker + 空格 + 数字）形式。

**影响**：之前 tables 解析工具不识别带空格的形式，多组响应表全部漏抓（4.2.39 漏 180 字段 / 4.4.27 漏一部分）。已在 extractor 侧修复。

**建议**：可以保留现写法（已兼容），但更稳妥是统一成 `请求示例1` 无空格形式。

### D4. 表标题不以"参数列表"结尾

**现状**：
- 4.4.7 `表4-712 支持自定义调速的刀片列表`（首列是刀片型号，不是参数）
- 4.2.39 `表4-166 语言、键盘、时区示例` / `表4-167 Position参数示例`（示例表，非参数表）

**影响**：之前会被解析工具误吃进上一张参数表 → 误抓为参数（4.4.7 把 `TS200-2280`、`X6800` 等 32 个刀片型号当 body 参数）。已在 extractor 侧修复。

**建议**：保留现表标题即可（extractor 已能识别"表X-YYY ..."形式作为表边界）。但若要长期稳健，建议表标题统一 `表X-YYY <用途>列表` 命名。

### D5. 4.1.7 "响应参数：无" 但响应示例有 60+ 字段

**现状**：响应参数段写了一个字"无"，但响应示例段含两个完整的 JSON schema（HwVncService、Volume），共 60+ 字段。

**影响**：tables 抓出 response=0，examples 抓出 response=60+，对比时显示差异巨大。

**建议**：补完整的"响应参数表"，列出 schema 文件返回的关键字段；或在响应参数段说明"返回值为 schema JSON 文件，结构请参考响应示例"。

---

## 类型 E — JSON 示例语法错误

### E1. JSON 用 `]` 误代替 `}`

**4.3.3 修改指定系统资源属性** 响应示例 JSON：
```json
"TrustedModules": [
    {
        ...
        "state": "Absent"
    }
],     ← 这一行 `]` 是错误的，应该是 `}`（先关 dict 元素，再关 array）
"Oem": { ... }
```

**建议**：把 `]` 改成 `}`，并在最后正确收尾 array。**4.3.2 同样问题**，请同步修。

### E2. `&nbsp;` HTML 实体嵌入 JSON

**4.3.2 / 4.3.3** 响应示例 JSON 中出现 `"ConfigurationModel":&nbsp;"2025V1"`、`"SystemType":&nbsp;"Physical"` 等。

**建议**：把所有 `&nbsp;` 替换成普通空格。这通常是从 Word/HTML 复制时引入的。

### E3. 其它疑似 JSON 格式问题

- 4.2.46 响应示例里 `"SASSmartInformation": {...}` 之后的 `"BDF"` 行缩进错位、缺逗号
- 部分 JSON 示例末尾整段 `{` 没合
- （需要在 doc 编辑后用 `json.loads` 全量校验所有响应示例）

**建议**：用 `python -c 'import json,sys; json.loads(sys.stdin.read())'` 把每个响应示例 JSON 拷出来验证一遍，发现就改。

---

## 类型 F — 响应表 vs 响应示例字段集合不一致（汇总）

`output/param_diff.txt` 显示 370 条接口里 ~280 条接口的 response 字段集合两边有差。这分两种情况：

1. **不算 doc bug**：tables 写完整 schema、examples 只展示一种典型响应——这是 schema vs 实例的本质差异。
2. **可能是 doc bug**：response 表少列字段、或响应示例字段未在 schema 表里出现。

差异最大的 top 接口（`output/param_diff.txt` 里"参数有差异的 section 明细"段可见全部）：

| section | tables response | examples response | 备注 |
|---|---:|---:|---|
| 4.4.27 查询指定驱动器资源信息 | 216 | 90 | 4 张响应表（SAS/SATA/SD/PCIe）合并，重复多 |
| 4.3.3 修改指定系统资源属性 | 179 | 131 | 含 E1、E2 JSON 语法 bug |
| 4.3.2 查询指定系统资源信息 | 191 | 124 | 同上 |
| 4.2.39 创建SP服务的OS安装配置 | 180 | 73 | 5 组响应表合并 |
| 4.4.7 修改指定机柜散热资源信息 | 103 | 89 | |
| 4.3.51 查询指定处理器资源信息 | 128 | 98 | |
| 4.2.2 查询指定管理资源信息 | 110 | 81 | 含 C 类前缀差异 |
| 4.10.7.4 查询指定CA证书的资源信息 | 54 | 31 | |

**建议**：F 类不需要逐条修文档，但建议安排一次"schema vs 真实响应"的 audit——对差异大的接口用真实环境抓取一次响应 JSON，对照 schema 表查漏补缺。

---

## 修订优先级建议

按客户端使用影响排序：

| 优先级 | 类型 | 说明 |
|---|---|---|
| **P0** | A1 / A2 / A3 / A4 / A5 | URI 错误，客户端按 doc 拼出来直接 404 |
| **P0** | A8 | method 错，客户端发请求被拒 |
| **P1** | A6 / A7 | URI 用具体值或路径不一致，客户端无法泛化 |
| **P1** | B1 / B2 / B3 | 字段名拼错或大小写错，客户端找不到字段 |
| **P1** | E1 / E2 | JSON 不能 parse，自动化工具失败 |
| **P2** | C | Action 前缀写法不统一，按 Redfish 规范修 |
| **P2** | D1 | 4.10.4.2 缺首行（自动化工具丢条目）|
| **P3** | D2 / D3 / D4 | extractor 已经兼容，但建议长期统一 |
| **P3** | F | schema vs 实例 audit，工作量大 |
