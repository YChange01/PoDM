# BMC vs PoDManager 跨文档对比报告

## 总览

| 维度 | 数值 |
|---|---:|
| PoDManager 接口数 | 371 |
| BMC 接口数 | 542 |
| 配对成功（共有接口）| **304** |
|  ├ 通过标题精确配对 | 257 |
|  ├ 通过 URI+method 配对 | 46 |
|  ├ 通过归一化 URI 配对 | 0 |
|  └ 通过路径骨架配对 | 1 |
| 仅 PoDManager（PoDM 独有）| 67 |
| 仅 BMC（BMC 独有）| 238 |
| 共有接口中 method 不一致 | 4 |
| 共有接口中归一化 URI 不一致 | 60 |
| 共有接口中参数集合有差异 | 225 |

## 共有接口：method 不一致（4 条）

| PoDM section | 标题 | PoDM | BMC |
|---|---|---|---|
| 4.2.39 | 创建SP服务的OS安装配置 | `GET` | `POST` |
| 4.2.58 | 创建SP服务的RAID配置 | `GET` | `POST` |
| 4.4.53 | 设置风扇组、泵组转速批量下发 | `GET` | `POST` |
| 4.9.15 | 修改指定触发器资源信息 | `GET` | `PATCH` |

## 共有接口：归一化 URI 不一致（60 条）

> 已经统一归一化（剥 https://device_ip + bare 占位符加 {}）后仍不同。

| section | 标题 | PoDM URI | BMC URI |
|---|---|---|---|
| 4.2.82 | 下载BMC文件 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 4.2.83 | 进入最小系统 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 4.3.11 | 查询虚拟媒体集合资源 | `/redfish/v1/Systems/{system_id}/VirtualMedia` | `/redfish/v1/Managers/{manager_id}/VirtualMedia` |
| 4.3.12 | 查询虚拟媒体资源 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD` | `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD` |
| 4.3.14 | 连接虚拟媒体 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Oem/Huawei/A` | `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD/Oem/Huawei` |
| 4.3.15 | 断开虚拟媒体 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Oem/Huawei/A` | `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD/Oem/Huawei` |
| 4.3.16 | 查询虚拟SP U盘资源 | `/redfish/v1/Systems/{system_id}/VirtualMedia/USBStick` | `/redfish/v1/Managers/{manager_id}/VirtualMedia/USBStick` |
| 4.2.7 | SNMP发送测试事件 | `redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpSer` | `/redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpSe` |
| 4.3.8 | 查询KVM资源 | `/redfish/v1/Systems/{system_id}/KvmService` | `/redfish/v1/Managers/{manager_id}/KvmService` |
| 4.3.9 | 修改KVM资源属性 | `/redfish/v1/Systems/{system_id}/KvmService` | `/redfish/v1/Managers/{manager_id}/KvmService` |
| 4.3.10 | 设置KVM Key | `/redfish/v1/Systems/{system_id}/KvmService/Actions/KvmServic` | `/redfish/v1/Managers/{manager_id}/KvmService/Actions/KvmServ` |
| 4.10.8.2 | 更新系统主密钥 | `/redfish/v1/Managers/1/SecurityService/Actions/SecurityServi` | `/redfish/v1/Managers/{manager_id}/SecurityService/Actions/Se` |
| 4.10.2.7 | 查询SSL证书更新服务资源信息 | `/redfish/v1/Managers/1/SecurityService/CertUpdateService` | `/redfish/v1/Managers/{manager_id}/SecurityService/ CertUpdat` |
| 4.10.2.8 | 修改SSL证书更新服务资源信息 | `/redfish/v1/Managers/1/SecurityService/CertUpdateService` | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 4.3.6 | 查询VNC资源 | `/redfish/v1/Systems/{system_id}/VncService` | `/redfish/v1/Managers/{manager_id}/VncService` |
| 4.3.7 | 修改VNC资源属性 | `/redfish/v1/Systems/{system_id}/VncService` | `/redfish/v1/Managers/{manager_id}/VNCService` |
| 4.2.43 | 升级SP或者升级固件 | `/redfish/v1/Managers/{manager_id}/SPService/SPFWUpdate/{upda` | `/redfish/v1/Managers/{manager_id}/SPService/SPFWUpdate/{upda` |
| 4.2.61 | 查询SP插件资源 | `/redfish/v1/Managers/{manager_id}/SPService/Plugins/{plugin_` | `/redfish/v1/Managers/{manager_id}/SPService//Plugins/{plugin` |
| 4.2.62 | 删除SP插件资源 | `/redfish/v1/Managers/{manager_id}/SPService/Plugins/{plugin_` | `/redfish/v1/Managers/{manager_id}/SPService//Plugins/{plugin` |
| 4.2.25 | 导出日志信息 | `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_i` | `/redfish/v1/Managers/{manager_id}/LogServices/{logservice_id` |
| 4.2.26 | 查询日志集合资源信息 | `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_i` | `/redfish/v1/Managers/{manager_id}/LogServices/{logservice_id` |
| 4.2.27 | 查询日志资源信息 | `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_i` | `/redfish/v1/Managers/{manager_id}/LogServices/LogService_id/` |
| 4.2.95 | 报废处置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 4.10.7.3 | 查询CA证书集合资源信息 | `/redfish/v1/Managers/1/Certificates` | `/redfish/v1/Managers/{manager_id}/Certificates` |
| 4.2.101 | 设置BMC吊销版本列表 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 4.3.5 | FRU上下电控制 | `/redfish/v1/Systems/{system_id}/Actions/Oem/Huawei/ComputerS` | `/redfish/v1/Systems/{system_id}/Actions/Oem/Huawei/Public/Co` |
| 4.3.24 | 查询网络桥接资源信息 | `/redfish/v1/Systems/{system_id}/NetworkBridge/{bridge _id}` | `/redfish/v1/Systems/{system_id}/NetworkBridge/bridge _id` |
| 4.4.58 | 查询电子保单信息 | `/redfish/v1/Chassis/{chassis_id}/DigitalWarranty` | `/redfish/v1/Systems/{system_id}/DigitalWarranty` |
| 4.4.59 | 修改电子保单信息 | `/redfish/v1/Chassis/{chassis_id}/DigitalWarranty` | `/redfish/v1/Systems/{system_id}/DigitalWarranty` |
| 4.3.13 | 设置虚拟媒体资源 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD` | `/redfish/v1/Systems/system_id /VirtualMedia/CD` |
| 4.4.5 | 恢复超节点配置信息为默认值 | `/redfish/v1/Chassis/{chassis_id}/Oem/Huawei/Actions/Chassis.` | `/redfish/v1/Chassis/Chassis_id/Oem/Huawei/Public/Actions/Cha` |
| 4.4.11 | 清空历史功率数据 | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Actions/Po` | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Act` |
| 4.4.12 | 重新统计功率数据 | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Actions/Po` | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Act` |
| 4.4.13 | 收集功率统计数据 | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Actions/Po` | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Act` |
| 4.4.17 | 查询电源转换器集合资源信息 | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/Oem/Huawei/P` | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/Oem/Huawei/P` |
| 4.4.18 | 查询电源转换器单个资源信息 | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/Oem/Huawei/P` | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/Oem/Huawei/P` |
| 4.4.27 | 查询指定驱动器资源信息 | `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}` | `/redfish/v1/Chassis/{chassis_id}/{drives}/{drive_id}` |
| 4.4.28 | 修改指定驱动器属性 | `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}` | `/redfish/v1/Chassis/{chassis_id}/Drives/{drives_id}` |
| 4.4.29 | 加密盘的数据安全擦除 | `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}/Actions/O` | `/redfish/v1/Chassis/{chassis_id}/Drives/{drives_id}/Actions/` |
| 4.4.33 | NPU模组复位 | `/redfish/v1/Chassis/{chassis_id}/Boards/ACUBoard/Actions/Npu` | `/redfish/v1/Chassis/{chassis_id}/Boards/{board_id}/Actions/N` |
| 4.4.37 | 复位指定SDI卡 | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` |
| 4.4.38 | 设置指定SDI卡电源状态 | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` |
| 4.4.39 | 指定PCIe设备资源导入https证书 | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/pciedevices_id ` |
| 4.4.40 | 查询指定PCIe功能资源信息 | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` |
| 4.4.49 | 查询漏液检测器集合 | `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/LeakDetect` | `/redfish/v1/Chassis/{chassis_id}/LeakDetectors` |
| 4.4.50 | 查询漏液检测 | `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/LeakDetect` | `/redfish/v1/Chassis/{chassis_id}/LeakDetectors/LeakDetector_` |
| 4.4.57 | 查询指定Sensor资源信息 | `/redfish/v1/Chassis/{chassis_id}/Sensors/{sensor_id}` | `/ redfish/v1/Chassis/{chassis_id}/Sensors/{sensor_id}` |
| 4.4.54 | 查询单个电源信息 | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/PowerSupplie` | `/redfish/v1/Chassis/ChassisId/PowerSubsystem/PowerSupplies/P` |
| 4.4.55 | 查询单个电源度量信息 | `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/PowerSupplie` | `/redfish/v1/Chassis/ChassisId/PowerSubsystem/PowerSupplies/P` |
| 4.5.5 | 生效固件 | `/redfish/v1/UpdateService/Actions/Oem/Huawei/UpdateService.S` | `/redfish/v1/UpdateService/Actions/Oem/Huawei/Public/UpdateSe` |

... 还有 10 条

## 共有接口参数差异（按类别）

| 类别 | 仅 PoDM 字段(接口数 / 字段总数) | 仅 BMC 字段(接口数 / 字段总数) |
|---|---:|---:|
| path | 32 接口 / 41 字段 | 27 接口 / 27 字段 |
| header | 85 接口 / 126 字段 | 18 接口 / 19 字段 |
| body | 23 接口 / 77 字段 | 58 接口 / 447 字段 |
| query | 0 接口 / 0 字段 | 1 接口 / 5 字段 |
| response | 110 接口 / 348 字段 | 163 接口 / 2056 字段 |

## PoDManager 修订建议（按 BMC 字段补充优先级）

> 选取 BMC 同名接口比 PoDM 多出 ≥3 个字段、且字段名有 Redfish 标准感（非业务私属）的条目。可直接拿来评估 PoDM 是否需要补响应字段。

### 按 response 字段缺失数排序 top 30（共 97 条候选）

| PoDM section | 标题 | 缺失数 | BMC 多出来的字段（前 10）|
|---|---|---:|---|
| 4.3.41 | 查询BIOS资源信息 | 1003 | `ADDDCEn`, `AESEnable`, `APDEn`, `APEIEinjType`, `APEISupport`, `ARIEnable`, `ATS`, `AcpiApicPolicy`, `AcpiHPETEnable`, `AcpiHpet` ... +993 |
| 4.4.2 | 查询指定机柜资源信息 | 56 | `AssetOwner`, `AvailableRackSpaceU`, `BackupBatteryUnits`, `BasicRackSN`, `Board`, `Building`, `BunchId`, `BunchType`, `CabinetSerialNumber`, `Chassis` ... +46 |
| 4.2.46 | 查询SP服务的配置结果资源 | 55 | `Aborted`, `ActualTestResult`, `AssetVerification`, `CPUID`, `CPU详细信息`, `Cancelled`, `Cancelling`, `Capacity`, `ClockSpeed`, `Completed` ... +45 |
| 4.10.2.1 | 查询账户策略 | 49 | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `CertificateRevocationCheckEnabled` ... +39 |
| 4.10.2.2 | 修改账户策略 | 46 | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `Certificates` ... +36 |
| 4.7.7 | 创建事件订阅资源 | 31 | `@Redfish.ActionInfo`, `@odata.context`, `@odata.id`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `Context`, `DeliveryRetryPolicy`, `Destination` ... +21 |
| 4.1.2 | 查询当前根服务资源 | 27 | `ComponentIntegrity`, `DeepOperations`, `DeepPATCH`, `DeepPOST`, `ExcerptQuery`, `ExpandAll`, `ExpandQuery`, `Fabrics`, `FilterQuery`, `FilterQueryComparisonOperations` ... +17 |
| 4.7.3 | 模拟测试事件 | 25 | `@odata.context`, `@odata.id`, `Addinfo`, `Context`, `EventId`, `EventSubject`, `EventTimestamp`, `EventType`, `Events`, `Id` ... +15 |
| 4.2.19 | 查询PoDManager指定网卡信息 | 24 | `AdaptiveFlag`, `AdaptivePort`, `Chassis`, `ChassisLanSubNet`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link` ... +14 |
| 4.2.16 | 查询PoDManager服务信息 | 23 | `AccessMode`, `Certificates`, `Certificates.@odata.id`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `FQDN`, `HideCommunityStrings` ... +13 |
| 4.3.2 | 查询指定系统资源信息 | 22 | `ActivatedSessionsType`, `AutoOSLockEnabled`, `AutoOSLockKey`, `AutoOSLockType`, `BSasCtrlSdkVersion`, `BWUWaveTitle`, `DelaySecondsAfterCpuThermalTrip`, `DisableKeyboardDuringBiosStartup`, `EnergySavingEnabled`, `HotSpare` ... +12 |
| 4.7.8 | 查询事件订阅资源 | 21 | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription` ... +11 |
| 4.7.9 | 修改事件订阅资源 | 21 | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription` ... +11 |
| 4.2.20 | 修改指定PoDManager网卡信息 | 20 | `AdaptiveFlag`, `AdaptivePort`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link`, `ManagementNetworkPort`, `ManagementNetworkPort@Redfish.AllowableValues` ... +10 |
| 4.2.4 | 查看SNMP资源信息 | 19 | `@Redfish.ActionInfo`, `Actions`, `BobEnabled`, `Links`, `LoginRule`, `LongPasswordEnabled`, `PasswordPattern`, `PasswordRulePolicy`, `RWCommunityEnabled`, `ReadOnlyCommunity` ... +9 |
| 4.10.1.4 | 查询全量用户 | 19 | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `KeyUsage`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `PublicKeyLengthBits` ... +9 |
| 4.5.1 | 查询升级服务资源信息 | 18 | `@Redfish.ActionInfo`, `AutoFirmwareActivationEnable`, `CertificateRevocationLists`, `Certificates`, `FirmwareIntegrity`, `FirmwareToTakeEffect`, `FirmwareType`, `InbandFirmwareUpdateEnabled`, `MaxImageSizeBytes`, `RelatedFirmwareItems` ... +8 |
| 4.10.1.2 | 修改用户 | 17 | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `RevokedDate`, `RevokedState` ... +7 |
| 4.3.51 | 查询指定处理器资源信息 | 15 | `AggregateTotalCount`, `BandWidth`, `Bank`, `Boards`, `ErrorCount`, `Family`, `Metrics`, `NpuBoardSerialNumber`, `OtherParameters`, `PhysicalAddress` ... +5 |
| 4.2.17 | 修改PoDManager服务信息 | 15 | `AccessMode`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `HideCommunityStrings`, `HttpProtocolVersion`, `NTPServers`, `NetworkSuppliedServers` ... +5 |
| 4.10.2.7 | 查询SSL证书更新服务资源信息 | 14 | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber` ... +4 |
| 4.10.2.8 | 修改SSL证书更新服务资源信息 | 14 | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber` ... +4 |
| 4.10.1.5 | 查询指定用户 | 14 | `@Redfish.ActionInfo`, `FingerPrint`, `HostBootstrapAccount`, `IssueBy`, `IssueTo`, `LastLoginIp`, `RevokedDate`, `RevokedState`, `RootCertUploadedState`, `SSHPublicKeyHash` ... +4 |
| 4.6.3 | 查询指定任务资源信息 | 13 | `Description`, `EndTime`, `EstimatedDuration`, `Message`, `MessageArgs`, `MessageId`, `MessageSeverity`, `Messages`, `PercentComplete`, `RelatedProperties` ... +3 |
| 4.2.75 | 查询全量告警信息 | 12 | `Created`, `EntryType`, `EventId`, `EventSubject`, `EventType`, `HandlingSuggestion`, `Level`, `Message`, `MessageArgs`, `MessageId` ... +2 |
| 4.4.25 | 查询网络端口上接的光模块资源信息 | 12 | `@Redfish.ActionInfo`, `Actions`, `ContaminationDetection`, `LaneMappings`, `Location`, `LocationOrdinalValue`, `LocationType`, `PartLocation`, `PartLocationContext`, `RXFCSErrors` ... +2 |
| 4.4.20 | 查询网络适配器单个资源信息 | 11 | `Actions`, `Assembly`, `Metrics`, `NetworkDeviceFunctions`, `Ports`, `PreloadPortCount`, `PreloadPortCountAllowableValues`, `Processors`, `RootBDFs`, `SerialNumber` ... +1 |
| 4.10.7.1 | 导入CA证书 | 11 | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState` ... +1 |
| 4.4.3 | 修改指定机柜资源信息 | 11 | `BackupBatteryUnits`, `Board`, `Chassis`, `ChassisLocation`, `ManufacturingDate`, `MezzCardNum`, `Presence`, `ProductName`, `SDCardNum`, `SDContollerNum` ... +1 |
| 4.10.7.5 | 导入CA证书吊销列表 | 11 | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState` ... +1 |

## 仅 PoDManager 有 / BMC 无（67 条）

> 这些接口可能是 PoDM 特有，或 BMC 用了不同的标题 / URI 没匹配上。建议人工核对一遍。

| section | method | 标题 | URI |
|---|---|---|---|
| 4.1.11 | GET | 查询机柜概览信息 | `/redfish/v1/ChassisOverview` |
| 4.1.13 | GET | 查询逻辑计算节点配比信息 | `/redfish/v1/Oem/Huawei/ResourceNodes` |
| 4.10.1.6 | POST | 二次认证 | `/redfish/v1/AccountService/{check}` |
| 4.10.2.10 | PATCH | 修改密钥策略 | `/redfish/v1/Managers/1/SecurityService` |
| 4.10.2.11 | PATCH | 修改南向SSL证书更新服务资源信息 | `/redfish/v1/Managers/1/SecurityService/SouthCertUpdateServic` |
| 4.10.2.12 | GET | 查询南向SSL证书更新服务资源信息 | `/redfish/v1/Managers/1/SecurityService/SouthCertUpdateServic` |
| 4.10.2.9 | GET | 查询密钥策略 | `/redfish/v1/Managers/1/SecurityService` |
| 4.10.4.5 | GET | 会话续约 | `/redfish/v1/SessionService/Actions/SessionService.CheckValid` |
| 4.10.5.1 | POST | 导入SSL自定义证书 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.5.2 | GET | 查询SSL证书 | `/redfish/v1/Managers/1/SecurityService/HttpsCert` |
| 4.10.5.3 | POST | CSR生成 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.5.4 | GET | CSR导出 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.5.5 | POST | 导入SSL服务器证书 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.5.6 | GET | SSL证书在线更新 | `/redfish/v1/Managers/1/SecurityService/CertUpdateService/Act` |
| 4.10.6.1 | POST | 导入南向SSL自定义证书 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.6.2 | GET | 查询南向SSL证书 | `/redfish/v1/Managers/1/SecurityService/HttpsSouthCert` |
| 4.10.6.3 | POST | 南向证书CSR生成 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.6.4 | GET | 南向证书CSR导出 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.6.5 | POST | 导入南向SSL服务器证书 | `/redfish/v1/Managers/1/SecurityService/HttpsCert/Actions/Htt` |
| 4.10.6.6 | POST | 南向SSL证书在线更新 | `/redfish/v1/Managers/1/SecurityService/CertUpdateService/Act` |
| 4.10.6.7 | POST | 导入南向设备SSL自定义证书 | `/redfish/v1/Managers/BladeN/SecurityService/HttpsCert/Action` |
| 4.10.6.8 | POST | 导入南向设备SSL服务证书 | `/redfish/v1/Managers/BladeN/SecurityService/HttpsCert/Action` |
| 4.10.6.9 | POST | 导入南向设备CA证书 | `/redfish/v1/CertificateService/Actions/CertificateService.Im` |
| 4.10.7.4 | GET | 查询指定CA证书的资源信息 | `/redfish/v1/Managers/1/Certificates/{certificate_id}` |
| 4.10.7.6 | POST | 删除CA证书吊销列表 | `/redfish/v1/CertificateService/Actions/CertificateService.De` |
| 4.10.8.1 | GET | 查询系统主密钥 | `/redfish/v1/Managers/1/SecurityService/Actions/SecurityServi` |
| 4.11.1 | GET | 查询UBMService资源 | `/redfish/v1/Oem/Huawei/UBMService` |
| 4.11.2 | GET | 查询UBM设备集合信息 | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices` |
| 4.11.3 | GET | 查询指定UBM设备信息 | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices/{device_id}` |
| 4.11.4 | PATCH | 修改指定UBM设备信息 | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices/{device_id}` |
| 4.11.5 | GET | 查询UBM设备子卡集合信息 | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices/{device_id}/Sub` |
| 4.11.6 | GET | 查询指定UBM设备子卡信息 | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices/{device_id}/Sub` |
| 4.11.7 | POST | 导出指定UBM设备日志 (待更新) | `/redfish/v1/Oem/Huawei/UBMService/UBMDevices/{device_id}/Act` |
| 4.2.100 | POST | 下发入侵检测配置信息 （未实现） | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.102 | POST | 启动纳管 | `/redfish/v1/Managers/SMN1(SMN2) /Actions/Oem/Huawei/Manager.` |
| 4.2.103 | POST | 上载GESwtich文件 | `/redfish/v1/Managers/SMN1(SMN2)/Actions/Oem/Huawei/Manager.I` |
| 4.2.104 | POST | 上载UBM文件 | `/redfish/v1/Managers//SMN1(SMN2) /Actions/Oem/Huawei/Manager` |
| 4.2.105 | POST | 上载文件 | `/redfish/v1/Managers/SMN1(SMN2) /Actions/Oem/Huawei/Manager.` |
| 4.2.106 | POST | 设置整柜的维护状态，抑制整柜告警上报 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.107 | POST | 设置刀片的维护状态，抑制刀片告警上报 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.108 | GET | 查询刀片维护状态 | `/redfish/v1/Managers/{manager_id}/Oem/Huawei/MaintenanceMode` |
| 4.2.117 | POST | 导入刀片配置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.118 | POST | 导出刀片配置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.119 | POST | 备份刀片配置文件 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.120 | POST | 还原刀片配置文件 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.121 | POST | 添加删除黑白名单命令的IPMI命令表（未评审） | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.14 | GET | 查询网口模式信息 | `/redfish/v1/Managers/{manager_id}/EthernetInterfaces/Oem/Hua` |
| 4.2.15 | POST | 设置网口模式信息 | `/redfish/v1/{managers}/{manager_id}/Oem/Huawei/Manager.SetEt` |
| 4.2.30 | POST | 导出整框配置数据 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.31 | POST | 文件下载 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.32 | POST | 导入整框配置数据 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.33 | POST | 固件文件上传 | `/redfish/v1/Managers/{manager_id}/UpdateService/FirmwareInve` |
| 4.2.6 | POST | 修改指定用户SNMP v3加密密码（未实现） | `redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpSer` |
| 4.2.65 | POST | 下发整柜ETH链路压测 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/SwtichDi` |
| 4.2.66 | GET | 查询整柜ETH链路压测结果 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/SwtichDi` |
| 4.2.67 | POST | 下发整柜压测 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/UBDiagno` |
| 4.2.68 | GET | 查询整柜压测结果 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/UBDiagno` |
| 4.2.76 | GET | 查询当前告警信息 | `/redfish/v1/Managers/{manager_id}/LogServices/EventLog/Oem/H` |
| 4.2.79 | POST | 重启GESWITCH | `/redfish/v1/Managers/{manager_id}/GESwitch/Actions/GESwitchS` |
| 4.2.8 | POST | 导出整柜日志 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.80 | POST | 恢复刀片出厂设置 | `/redfish/v1/Managers/{manager_id}/Actions/Manager.RestoreFac` |
| 4.2.81 | POST | 恢复整框出厂设置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.2.85 | POST | 切换PoDManager镜像 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager` |
| 4.4.4 | POST | 控制机柜定位指示灯状态 | `/redfish/v1/Chassis/{Chassis_id}/Oem/Huawei/Public/Actions/C` |
| 4.4.42 | POST | 查询历史功率资源信息 | `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Act` |
| 4.4.8 | POST | 清空进风口历史温度的数据 | `/redfish/v1/Chassis/{chassis_id}/Thermal/Oem/Huawei/Actions/` |
| 4.7.12 | POST | 设置事件告警上报级别 | `/redfish/v1/EventService/Actions/Oem/Huawei/EventService.Set` |

## 仅 BMC 有 / PoDManager 无（238 条）

> 这些是 BMC 比 PoDM 多的接口。如 PoDM 有相关功能但用了不同接口名/URI，可考虑对齐 BMC 命名。

| section | method | 标题 | URI |
|---|---|---|---|
| 3.1.11 | GET | 查询系统概览信息 | `/redfish/v1/SystemOverview` |
| 3.1.13 | GET | 查询归档的BMC事件上报注册文件资源 | `/redfish/v1/RegistryStore/Messages/{en}/{file_id}` |
| 3.10.1 | GET | 查询升级服务资源 | `/redfish/v1/Sms/1/UpdateService` |
| 3.10.10 | POST | 文件上传操作 | `/redfish/v1/Sms/1/UpdateService/Actions/UpdateService.Upload` |
| 3.10.11 | GET | 查询任务服务资源信息 | `/redfish/v1/Sms/1/TaskService` |
| 3.10.12 | GET | 查询任务集合资源信息 | `/redfish/v1/Sms/1/TaskService/Tasks` |
| 3.10.13 | GET | 查询指定任务资源信息 | `/redfish/v1/Sms/1/TaskService/Tasks/{taskid}` |
| 3.10.14 | POST | 收集日志资源 | `/redfish/v1/Sms/1/Systems/1/LogServices/iBMA/Actions/LogServ` |
| 3.10.15 | POST | 带内事件上报 | `/redfish/v1/Eventclient/Sms0` |
| 3.10.2 | POST | 带内升级软件/固件 | `/redfish/v1/Sms/1/UpdateService/Actions/UpdateService.Simple` |
| 3.10.3 | GET | 查询升级进度 | `/redfish/v1/Sms/1/UpdateService/Progress` |
| 3.10.4 | GET | 查询带内升级软件集合资源信息 | `/redfish/v1/Sms/1/UpdateService/SoftwareInventory` |
| 3.10.5 | GET | 查询指定带内升级软件资源信息 | `/redfish/v1/Sms/1/UpdateService/SoftwareInventory/{item}` |
| 3.10.6 | GET | 查询带内升级固件集合资源信息 | `/redfish/v1/Sms/1/UpdateService/FirmwareInventory` |
| 3.10.7 | GET | 查询指定带内升级固件资源信息 | `/redfish/v1/Sms/1/UpdateService/FirmwareInventory/{item}` |
| 3.10.8 | POST | 异步升级操作 | `/redfish/v1/Sms/1/UpdateService/Actions/UpdateService.Asynch` |
| 3.10.9 | POST | 异步升级生效 | `/redfish/v1/Sms/1/UpdateService/Actions/UpdateService.Effect` |
| 3.11.10 | GET | 查询数据表筛选结果 | `/redfish/v1/TaskService/Tasks/{task_id}/Monitor` |
| 3.11.3 | POST | 导出数据表 | `/redfish/v1/DataAcquisitionService/Actions/HwDataAcquisition` |
| 3.11.5 | GET | 查询导出表 | `/redfish/v1/TaskService/Tasks/{task_id}/Monitor` |
| 3.11.9 | POST | 创建数据表格筛选任务 | `/redfish/v1/DataAcquisitionService/Actions/HwDataAcquisition` |
| 3.12.3 | GET | 查询证书路径信息 | `/redfish/v1/CertificateService/CertificateLocations` |
| 3.12.7 | POST | 生成CSR | `/redfish/v1/CertificateService/Actions/CertificateService.Ge` |
| 3.12.8 | POST | 替换证书 | `/redfish/v1/CertificateService/Actions/CertificateService.Re` |
| 3.14.1 | GET | 查询编排任务服务信息 | `/redfish/v1/JobService` |
| 3.14.2 | PATCH | 修改编排任务服务信息 | `/redfish/v1/JobService` |
| 3.14.3 | GET | 查询编排任务集合信息 | `/redfish/v1/JobService/Jobs` |
| 3.14.4 | POST | 创建编排任务 | `/redfish/v1/JobService/Jobs` |
| 3.14.5 | GET | 查询指定编排任务信息 | `/redfish/v1/JobService/Jobs/{job_id}` |
| 3.14.6 | PATCH | 修改指定编排任务信息 | `/redfish/v1/JobService/Jobs/{job_id}` |
| 3.14.7 | DELETE | 删除指定编排任务信息 | `/redfish/v1/JobService/Jobs/{job_id}` |
| 3.16.1 | GET | 查询LCNService资源 | `/redfish/v1/Oem/Huawei/LCNService` |
| 3.16.10 | POST | 设置指定LCN设备的网络接口 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Act` |
| 3.16.11 | POST | 创建指定LCN设备的用户 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Acc` |
| 3.16.12 | POST | 删除指定LCN设备的用户 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Acc` |
| 3.16.13 | POST | 修改指定LCN设备的用户密码 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Acc` |
| 3.16.14 | POST | 重启指定LCN设备 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Act` |
| 3.16.15 | POST | 重启指定LCN设备并恢复默认出厂配置 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Act` |
| 3.16.16 | GET | 查询指定LCN设备升级服务的资源信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Upd` |
| 3.16.17 | POST | 升级指定LCN设备的系统软件 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Upd` |
| 3.16.2 | GET | 查询LCN设备集合信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices` |
| 3.16.3 | GET | 查询指定LCN设备信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}` |
| 3.16.4 | PATCH | 修改指定LCN设备信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}` |
| 3.16.5 | GET | 查询LCN设备子卡集合信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Sub` |
| 3.16.6 | GET | 查询指定LCN设备子卡信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Sub` |
| 3.16.7 | GET | 查询LCN设备用户信息 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Acc` |
| 3.16.8 | POST | 导出指定LCN设备日志 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Act` |
| 3.16.9 | POST | 设置与指定LCN设备通信的内部网络 | `/redfish/v1/Oem/Huawei/LCNService/LCNDevices/{device_id}/Act` |
| 3.17.1 | GET | 查询可观测服务配置资源 | `/redfish/v1/Oem/Huawei/Public/ObservabilityService` |
| 3.17.2 | PATCH | 设置可观测服务配置资源 | `/redfish/v1/Oem/Huawei/Public/ObservabilityService` |
| 3.17.3 | POST | 发送可观测服务测试报文 | `/redfish/v1/Oem/Huawei/Public/ObservabilityService/Actions/O` |
| 3.18.1 | GET | 查询电路集合资源信息 | `/redfish/v1/PowerEquipment/PowerShelves/{power_distribution_` |
| 3.18.2 | GET | 查询电路单个资源信息 | `/redfish/v1/PowerEquipment/PowerShelves/{power_distribution_` |
| 3.19.1 | GET | 查询组件完整性报告集合资源信息 | `/redfish/v1/ComponentIntegrity` |
| 3.19.2 | GET | 查询组件完整性报告单个资源信息 | `/redfish/v1/ComponentIntegrity/{component_integrity_id}` |
| 3.19.3 | POST | 基于SPDM协议获取组件签名测量值 | `/redfish/v1/ComponentIntegrity/{component_integrity_id}/Acti` |
| 3.2.108 | POST | 导出NPU日志 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/` |
| 3.2.109 | POST | 导出NPU运行日志 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/` |
| 3.2.110 | GET | 查询工作记录信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/WorkReco` |
| 3.2.119 | GET | 查询License服务信息 | `/redfish/v1/Managers/{manager_id}/LicenseService` |
| 3.2.120 | POST | 安装license | `/redfish/v1/Managers/{manager_id}/LicenseService/Actions/Lic` |
| 3.2.121 | POST | 导出license | `/redfish/v1/Managers/{manager_id}/LicenseService/Actions/Lic` |
| 3.2.122 | POST | 失效license | `/redfish/v1/Managers/{manager_id}/LicenseService/Actions/Lic` |
| 3.2.123 | POST | 删除license | `/redfish/v1/Managers/{manager_id}/LicenseService/Actions/Lic` |
| 3.2.126 | GET | 查询NIC集合资源 | `/redfish/v1/Managers/{manager_id}/NICs` |
| 3.2.127 | GET | 查询指定NIC资源 | `/redfish/v1/Managers/{manager_id}/NICs/{nicid}` |
| 3.2.128 | PATCH | 修改指定NIC资源 | `/redfish/v1/Managers/{manager_id}/NICs/{nicid}` |
| 3.2.131 | GET | 查询SMS服务资源信息 | `/redfish/v1/Managers/{manager_id}/SmsService` |
| 3.2.132 | PATCH | 修改SMS服务资源信息 | `/redfish/v1/Managers/{manager_id}/SmsService` |
| 3.2.133 | POST | 刷新可安装的BMA | `/redfish/v1/Managers/{manager_id}/SmsService/Actions/SmsServ` |
| 3.2.143 | GET | 查询DICE证书资源信息 | `/redfish/v1/Managers/{manager_id}/SecurityService/DiceCert` |
| 3.2.144 | POST | 导出DICE CSR | `/redfish/v1/Managers/{manager_id}/SecurityService/DiceCert/A` |
| 3.2.145 | POST | 导入DICE证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/DiceCert/A` |
| 3.2.146 | POST | 导出DICE证书链 | `/redfish/v1/Managers/{manager_id}/SecurityService/DiceCert/A` |
| 3.2.147 | POST | 导出融合身份认证证书链 | `/redfish/v1/Managers/{manager_id}/SecurityService/DiceCert/A` |
| 3.2.151 | GET | 查询指定CA证书资源信息 | `/redfish/v1/Managers/{manager_id}/Certificates/{certificate_` |
| 3.2.152 | POST | 删除CA证书的吊销列表 | `/redfish/v1/Managers/{manager_id}/Certificates/{certificate_` |
| 3.2.154 | PATCH | 设置事件记录模式 | `/redfish/v1/Managers/{manager_id}/LogServices/EventLog` |
| 3.2.155 | GET | 查询PRBS测试接口集合的资源信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest` |
| 3.2.157 | GET | 查询单个PRBS测试对象信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest` |
| 3.2.162 | GET | 查询脏污检测接口集合的资源信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.163 | GET | 查询脏污检测对象集合的资源信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.164 | GET | 查询单个脏污检测对象信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.165 | POST | 查询脏污检测信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.166 | POST | 初始化脏污检测 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.167 | POST | 启动脏污检测 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.168 | POST | 终止脏污检测 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Contamin` |
| 3.2.169 | POST | 下发入侵检测配置信息 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.17 | GET | 查询虚拟iBMA U盘资源 | `/redfish/v1/Managers/{manager_id}/VirtualMedia/iBMAUSBStick` |
| 3.2.172 | POST | 清空日志信息 | `/redfish/v1/Managers/{manager_id}/LogServices/EventLog/Actio` |
| 3.2.174 | POST | 恢复出厂设置 | `/redfish/v1/Managers/{manager_id}/Actions/Manager.ResetToDef` |
| 3.2.175 | POST | 测试文件服务器连通性 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.176 | GET | 查询SSL证书集合资源信息 | `/redfish/v1/Managers/{manager_id}/NetworkProtocol/HTTPS/Cert` |
| 3.2.177 | GET | 查询指定SSL证书资源信息 | `/redfish/v1/Managers/{manager_id}/NetworkProtocol/HTTPS/Cert` |
| 3.2.178 | POST | 导出诊断度量数据 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/` |
| 3.2.179 | POST | 收集硬盘日志信息 | `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/` |
| 3.2.18 | POST | 连接虚拟iBMA U盘 | `/redfish/v1/Managers/{manager_id}/VirtualMedia/iBMAUSBStick/` |
| 3.2.180 | GET | 查询节能策略资源信息 | `/redfish/v1/Managers/{manager_id}/EnergySavingService/Measur` |
| 3.2.181 | PATCH | 节能策略资源信息配置 | `/redfish/v1/Managers/{manager_id}/EnergySavingService/Measur` |
| 3.2.182 | GET | 查询CpuFPC服务资源 | `/redfish/v1/Managers/{manager_id}/FDMService/CpuFPC` |
| 3.2.183 | GET | 查询MemoryHighRAS内存健康状态信息 | `/redfish/v1/Managers/{manager_id}/FDMService/CpuFPC/MemoryHi` |
| 3.2.184 | POST | 执行内存隔离任务 | `/redfish/v1/Managers/{manager_id}/FDMService/CpuFPC/MemoryHi` |
| 3.2.185 | POST | 执行内存巡检任务 | `/redfish/v1/Managers/{manager_id}/FDMService/CpuFPC/MemoryHi` |
| 3.2.186 | GET | 查询NpuFPC服务资源 | `/redfish/v1/Managers/{manager_id}/FDMService/NpuFPC` |
| 3.2.187 | GET | 查询HBMHighRAS服务资源 | `/redfish/v1/Managers/{manager_id}/FDMService/NpuFPC/HBMHighR` |
| 3.2.188 | POST | 执行HBM巡检任务 | `/redfish/v1/Managers/{manager_id}/FDMService/NpuFPC/HBMHighR` |
| 3.2.19 | POST | 断开虚拟iBMA U盘 | `/redfish/v1/Managers/{manager_id}/VirtualMedia/iBMAUSBStick/` |
| 3.2.25 | POST | 修改指定用户SNMP v3加密密码 | `/redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpSe` |
| 3.2.27 | GET | 查询SMTP资源信息 | `/redfish/v1/Managers/{manager_id}/SmtpService` |
| 3.2.28 | PATCH | 修改SMTP资源属性 | `/redfish/v1/Managers/{manager_id}/SmtpService` |
| 3.2.29 | POST | 导入SMTP根证书 | `/redfish/v1/Managers/{manager_id}/SmtpService/Actions/SmtpSe` |
| 3.2.30 | POST | 发送SMTP测试邮件 | `/redfish/v1/Managers/{manager_id}/SmtpService/Actions/SmtpSe` |
| 3.2.33 | POST | 导入Syslog根证书 | `/redfish/v1/Managers/{manager_id}/SyslogService/Actions/Sysl` |
| 3.2.34 | POST | 导入Syslog本地证书 | `/redfish/v1/Managers/{manager_id}/SyslogService/Actions/Sysl` |
| 3.2.35 | POST | Syslog发送测试事件 | `/redfish/v1/Managers/{manager_id}/SyslogService/Actions/Sysl` |
| 3.2.36 | POST | 导入Syslog服务器证书吊销列表 | `/redfish/v1/Managers/{manager_id}/SyslogService/Actions/Sysl` |
| 3.2.37 | POST | 删除Syslog服务器证书吊销列表 | `/redfish/v1/Managers/{manager_id}/SyslogService/Actions/Sysl` |
| 3.2.4 | POST | 卸载语言 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.47 | POST | 切换iBMCBMC镜像 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.5 | POST | 恢复出厂设置（自定义接口） | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.50 | GET | 查询安全策略集合资源信息 | `/redfish/v1/Managers/{manager_id}/SecurityPolicy` |
| 3.2.51 | PATCH | 修改安全策略集合资源信息 | `/redfish/v1/Managers/{manager_id}/SecurityPolicy` |
| 3.2.53 | POST | 导入远程HTTPS传输服务器根证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/Actions/Se` |
| 3.2.54 | POST | 删除远程HTTPS传输服务器根证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/Actions/Se` |
| 3.2.55 | POST | 导入远程HTTPS传输服务器根证书的吊销列表 | `/redfish/v1/Managers/{manager_id}/SecurityService/Actions/Se` |
| 3.2.56 | GET | 查询SSL证书资源信息 | `/redfish/v1/Managers/{manager_id}/SecurityService/HttpsCert` |
| 3.2.57 | POST | 生成CSR | `/redfish/v1/Managers/{manager_id}/SecurityService/HttpsCert/` |
| 3.2.58 | POST | 导出CSR | `/redfish/v1/Managers/{manager_id}/SecurityService/HttpsCert/` |
| 3.2.59 | POST | 导入服务器证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/HttpsCert/` |
| 3.2.6 | POST | 一键收集 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.60 | POST | 导入自定义证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/HttpsCert/` |
| 3.2.63 | POST | 导入SSL证书更新服务的CA证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 3.2.64 | POST | 导入SSL证书更新服务的CA证书吊销列表 | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 3.2.65 | POST | 删除SSL证书更新服务的CA证书吊销列表 | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 3.2.66 | POST | 导入SSL证书更新服务的客户端证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 3.2.67 | POST | 更新BMC证书 | `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdate` |
| 3.2.7 | POST | 快速收集（精简日志收集） | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.8 | POST | 导入BIOS、BMC和RAID控制器配置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.2.9 | POST | 导出BIOS、BMC和RAID控制器配置 | `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/` |
| 3.3.22 | GET | 查询存储控制器集合资源信息 | `/redfish/v1/Systems/{system_id}/Storage/{storage_id}/Control` |
| 3.3.23 | GET | 查询指定存储控制器资源信息 | `/redfish/v1/Systems/{system_id}/Storage/{storage_id}/Control` |
| 3.3.26 | GET | 查询指定存储控制器指标资源信息 | `/redfish/v1/Systems/{system_id}/Storage/{storage_id}/Control` |
| 3.3.42 | POST | 导入安全启动证书 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.43 | POST | 重置安全启动证书 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.44 | POST | 导入HTTPS启动证书 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.45 | POST | 重置HTTPS启动证书 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.46 | POST | 导入HTTPS启动证书吊销列表 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.47 | POST | 重置HTTPS启动证书吊销列表 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.48 | GET | 查询Bios证书信息 | `/redfish/v1/Systems/{system_id}/Bios/Oem/Huawei/Public/BootC` |
| 3.3.52 | GET | 查询指定处理器指标资源信息 | `/redfish/v1/Systems/{system_id}/Processors/{processor_id}/Pr` |
| 3.3.53 | GET | 查询指定处理器端口集合资源信息 | `/redfish/v1/Systems/{system_id}/Processors/processor_id /Por` |
| 3.3.54 | GET | 查询处理器指定端口资源信息 | `/redfish/v1/Systems/{system_id}/Processors/processor_id /Por` |
| 3.3.58 | GET | 查询日志服务集合资源信息 | `/redfish/v1/Systems/{system_id}/LogServices` |
| 3.3.59 | GET | 查询指定日志服务资源信息 | `/redfish/v1/Systems/{system_id}/LogServices/{logservices_id}` |
| 3.3.60 | PATCH | 修改指定日志服务资源属性 | `/redfish/v1/Systems/{system_id}/LogServices/LogService_id` |
| 3.3.61 | POST | 清空日志信息 | `/redfish/v1/Systems/{system_id}/LogServices/LogService_id/Ac` |
| 3.3.62 | POST | 查询SEL日志 | `/redfish/v1/Systems/{system_id}/LogServices/LogService_id/Ac` |
| 3.3.63 | POST | 收集SEL日志 | `/redfish/v1/Systems/{systems_id}/LogServices/LogService_id/A` |
| 3.3.64 | GET | 查询日志集合资源信息 | `/redfish/v1/Systems/{system_id}/LogServices/Log_id/Entries` |
| 3.3.65 | GET | 查询日志资源信息 | `/redfish/v1/Systems/{system_id}/LogServices/LogService_id/En` |
| 3.3.75 | POST | 清除Foreign配置 | `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Action` |
| 3.3.78 | GET | 查询虚拟媒体集合资源 | `/redfish/v1/Systems/system_id /VirtualMedia` |
| 3.3.79 | GET | 查询虚拟媒体资源 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD` |
| 3.3.81 | POST | 连接虚拟媒体 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Actions/Virt` |
| 3.3.82 | POST | 断开虚拟媒体 | `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Actions/Virt` |
| 3.3.83 | GET | 查询安全启动资源信息 | `/redfish/v1/Systems/{system_id}/SecureBoot` |
| 3.3.84 | POST | 管理安全启动证书资源 | `/redfish/v1/Systems/{system_id}/SecureBoot/Actions/SecureBoo` |
| 3.3.85 | GET | 查询安全启动数据库集合资源信息 | `/redfish/v1/Systems/{system_id}/SecureBoot/SecureBootDatabas` |
| 3.3.86 | GET | 查询安全启动数据库资源信息 | `/redfish/v1/Systems/{system_id}/SecureBoot/SecureBootDatabas` |
| 3.3.87 | POST | 管理安全启动数据库中的安全启动证书资源 | `/redfish/v1/Systems/{system_id}/SecureBoot/SecureBootDatabas` |
| 3.3.88 | GET | 查询安全启动数据库安全启动证书集合信息 | `/redfish/v1/Systems/{system_id}/SecureBoot/SecureBootDatabas` |
| 3.3.89 | GET | 查询安全启动数据库中安全启动证书属性 | `/redfish/v1/Systems/{system_id}/SecureBoot/SecureBootDatabas` |
| 3.3.90 | POST | 清空内存指标资源当前周期的度量统计数据 | `/redfish/v1/Systems/{system_id}/Memory/{memory_id}/MemoryMet` |
| 3.3.91 | POST | 清空处理器指标资源当前周期的度量统计数据 | `/redfish/v1/Systems/{system_id}/Processors/{processor_id}/Pr` |
| 3.3.92 | GET | 查询图形控制器集合资源 | `/redfish/v1/Systems/{system_id}/GraphicsControllers` |
| 3.3.93 | GET | 查询指定图形控制器资源信息 | `/redfish/v1/Systems/{system_id}/GraphicsControllers/{graphic` |
| 3.4.20 | PATCH | 修改网络适配器单个资源信息 | `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{networkada` |
| 3.4.21 | GET | 查询单个网络适配器指标信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.22 | GET | 查询单个网络适配器组装信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.23 | GET | 查询单个网络适配器公开逻辑接口集合资源信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.24 | GET | 查询单个网络适配器的指定公开逻辑接口资源信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.25 | GET | 查询单个网络适配器的指定公开逻辑接口指标信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.26 | POST | 复位或上下电网络适配器 | `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{networkada` |
| 3.4.30 | GET | 查询单个网络端口度量信息 | `/redfish/v1/Chassis/Chassis_id/NetworkAdapters/{network_adap` |
| 3.4.33 | GET | 查询光模块通道映射关系集合资源信息 | `/redfish/v1/Chassis/{chassis_id}/Transceivers/{transceivers_` |
| 3.4.34 | GET | 查询光模块通道映射关系资源信息 | `/redfish/v1/Chassis/{chassis_id}/Transceivers/{transceivers_` |
| 3.4.38 | GET | 查询指定驱动器资源硬件诊断信息 | `/redfish/v1/Chassis/{chassis_id}/{drives}/{drive_id}/Metrics` |
| 3.4.39 | GET | 查询指定驱动器资源装配体信息 | `/redfish/v1/Chassis/{chassis_id}/{drives}/{drive_id}/Assembl` |
| 3.4.4 | GET | 查询指定机箱装配信息 | `/redfish/v1/Chassis/Chassis_id/Assembly` |
| 3.4.45 | GET | 查询PCIe插槽资源信息 | `/redfish/v1/Chassis/{chassis_id}/PCIeSlots` |
| 3.4.5 | POST | 控制机箱定位指示灯状态 | `/redfish/v1/Chassis/Chassis_id/Oem/Huawei/Public/Actions/Cha` |
| 3.4.52 | GET | 查询PCIe功能集合资源信息 | `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id` |
| 3.4.58 | GET | 查询备电集合资源信息 | `/redfish/v1/Chassis/{chassis_id}/BackupBatteryUnits` |
| 3.4.59 | GET | 查询备电单个资源信息 | `/redfish/v1/Chassis/{chassis_id}/BackupBatteryUnits/{backupb` |
| 3.4.73 | GET | 查询电源集合资源 | `/redfish/v1/Chassis/ChassisId/PowerSubsystem/PowerSupplies` |
| 3.4.76 | GET | 查询可信组件集合资源 | `/redfish/v1/Chassis/{chassis_id}/TrustedComponents` |
| 3.4.77 | GET | 查询可信组件单个资源信息 | `/redfish/v1/Chassis/{chassis_id}/TrustedComponents/{trusted_` |
| 3.4.78 | GET | 查询可信组件证书集合资源 | `/redfish/v1/Chassis/{chassis_id}/TrustedComponents/{trusted_` |
| 3.4.79 | GET | 查询可信组件单个证书资源信息 | `/redfish/v1/Chassis/{chassis_id}/TrustedComponents/{trusted_` |
| 3.4.80 | GET | 查询泵集合资源信息 | `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/Pumps` |
| 3.4.81 | GET | 查询泵单个资源信息 | `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/Pumps/{pum` |
| 3.4.82 | GET | 查询电子保单信息 | `/redfish/v1/Chassis/{chassis_id}/Oem/Public/Huawei/DigitalWa` |
| 3.4.83 | PATCH | 修改电子保单信息 | `/redfish/v1/Chassis/{chassis_id}/Oem/Public/Huawei/DigitalWa` |
| 3.4.84 | POST | 复位指定物理盘 | `/redfish/v1/Chassis/{chassis_id}/Drives/{drives_id}/Actions/` |
| 3.4.85 | POST | 控制光模块Active指示灯状态 | `/redfish/v1/Chassis/Chassis_id/Transceivers/{transceivers_id` |
| 3.4.9 | POST | 清空进风口历史温度数据 | `/redfish/v1/Chassis/{chassis_id}/Thermal/Oem/Huawei/Public/A` |
| 3.5.7 | POST | 创建Web会话 | `/redfish/v1/SessionService/Sessions` |
| 3.5.8 |  | Web执行操作 | `/redfish/v1/SessionService/Sessions` |
| 3.6.10 | POST | 双因素认证的用户的客户端证书导入 | `/redfish/v1/AccountService/Accounts/{account_id}/Oem/Huawei/` |
| 3.6.11 | POST | 双因素认证的用户的客户端证书删除 | `/redfish/v1/AccountService/Accounts/{account_id}/Oem/Huawei/` |
| 3.6.12 | POST | 双因素认证的客户端证书吊销列表导入 | `/redfish/v1/AccountService/Oem/Huawei/Public/Actions/Account` |
| 3.6.13 | POST | 双因素认证的客户端证书吊销列表删除 | `/redfish/v1/AccountService/Oem/Huawei/Public/Actions/Account` |
| 3.6.14 | POST | SSH公钥导入 | `/redfish/v1/AccountService/Accounts/{account_id}/Oem/Huawei/` |
| 3.6.15 | POST | SSH公钥删除 | `/redfish/v1/AccountService/Accounts/{account_id}/Oem/Huawei/` |
| 3.6.19 | POST | 创建自定义角色 | `/redfish/v1/AccountService/Roles` |
| 3.6.20 | DELETE | 删除自定义角色 | `/redfish/v1/AccountService/Roles/{role_id}` |
| 3.6.26 | POST | 具体域控制器Ldap证书的导入 | `/redfish/v1/AccountService/LdapService/LdapControllers/{memb` |
| 3.6.27 | POST | 具体域控制器Ldap服务器证书吊销列表导入 | `/redfish/v1/AccountService/LdapService/LdapControllers/{memb` |
| 3.6.28 | GET | 查询权限映射资源信息 | `/redfish/v1/AccountService/PrivilegeMap` |
| 3.6.29 | GET | 查询Kerberos服务资源 | `/redfish/v1/AccountService/KerberosService` |
| 3.6.30 | PATCH | 修改Kerberos功能开启使能 | `/redfish/v1/AccountService/KerberosService` |
| 3.6.31 | GET | 查询Kerberos域控制器集合信息 | `/redfish/v1/AccountService/KerberosService/KerberosControlle` |
| 3.6.32 | GET | 查询具体Kerberos域控制器的信息 | `/redfish/v1/AccountService/KerberosService/KerberosControlle` |
| 3.6.33 | PATCH | 修改具体Kerberos域控制器的信息 | `/redfish/v1/AccountService/KerberosService/KerberosControlle` |
| 3.6.34 | POST | 修改指定用户的密码 | `/redfish/v1/AccountService/Accounts/{member_id}/Actions/Mana` |
| 3.6.5 | POST | 创建新用户 | `/redfish/v1/AccountService/Accounts` |
| 3.6.8 | POST | 双因素认证的根证书导入 | `/redfish/v1/AccountService/Oem/Huawei/Public/Actions/Account` |
| 3.6.9 | POST | 双因素认证的根证书删除 | `/redfish/v1/AccountService/Oem/Huawei/Public/Actions/Account` |
| 3.7.10 | POST | 弃用暂存固件 | `/redfish/v1/UpdateService/Actions/Oem/Huawei/UpdateService.D` |
| 3.7.11 | GET | 查询固件更新服务能力信息 | `/redfish/v1/UpdateService/UpdateServiceCapabilities` |
| 3.7.12 | POST | 升级固件整包 | `/redfish/v1/UpdateService/Actions/Oem/Huawei/UpdateService.F` |
| 3.7.2 | PATCH | 修改升级服务信息 | `/redfish/v1/UpdateService` |
| 3.7.5 | POST | 升级固件 | `/redfish/v1/UpdateService/Actions/UpdateService.SimpleUpdate` |
| 3.7.9 | POST | 生效暂存固件 | `/redfish/v1/UpdateService/Actions/UpdateService.Activate` |
| 3.8.2 | PATCH | 修改任务服务资源信息 | `/redfish/v1/TaskService` |
| 3.9.12 | POST | 配置事件告警级别 | `/redfish/v1/EventService/Actions/Oem/Huawei/Public/EventServ` |
| 3.9.13 | POST | 恢复订阅事件信息 | `/redfish/v1/EventService/Subscriptions/{id}/Actions/EventDes` |
| 3.9.14 | POST | 暂停订阅事件信息 | `/redfish/v1/EventService/Subscriptions/{id}/Actions/EventDes` |

