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

## 共有接口参数差异 详细列表（共 225 条，按差异字段总数降序）

> 每条接口列出每个类别下「仅 PoDM 有」和「仅 BMC 有」的字段。空类别省略。

### 4.3.41 查询BIOS资源信息（差异 1004）

- BMC section: `3.3.33`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | `ADDDCEn`, `AESEnable`, `APDEn`, `APEIEinjType`, `APEISupport`, `ARIEnable`, `ATS`, `AcpiApicPolicy`, `AcpiHPETEnable`, `AcpiHpet`, `AcsEnable`, `ActiveCpuCores`, `AltEngPerfBIAS`, `ApdEn`, `AppDirectMemoryHole`, `ApplicationProfile`, `AttemptFastBootCold`, `Authority`, `AutoRefresh`, `AvxIccpLevel`, `BIOSSSABacksideMargining`, `BIOSSSACmdAll`, `BIOSSSACmdVref`, `BIOSSSACtlAll`, `BIOSSSADebugMessages`, `BIOSSSADisplayTables`, `BIOSSSAEarlyReadIdMargining`, `BIOSSSAEridDelay`, `BIOSSSAEridVref`, `BIOSSSALoopCount`, `BIOSSSAPerBitMargining`, `BIOSSSAPerDisplayPlots`, `BIOSSSARxDqs`, `BIOSSSARxVref`, `BIOSSSAStepSizeOverride`, `BIOSSSATxDq`, `BIOSSSATxVref`, `BIOS属性列表`, `BIOS资源信息`, `BMCWDTAction`, `BMCWDTEnable`, `BMCWDTTimeout`, `BenchMarkSelection`, `BiosSsaBacksideMargining`, `BiosSsaCmdAll`, `BiosSsaCmdVref`, `BiosSsaCtlAll`, `BiosSsaDebugMessages`, `BiosSsaDisplayTables`, `BiosSsaEarlyReadIdMargining`, `BiosSsaEridDelay`, `BiosSsaEridVref`, `BiosSsaLoopCount`, `BiosSsaPerBitMargining`, `BiosSsaPerDisplayPlots`, `BiosSsaRxDqs`, `BiosSsaRxVref`, `BiosSsaStepSizeOverride`, `BiosSsaTxDq`, `BiosSsaTxVref`, `BootFailPolicy`, `BootOverride`, `BootOverrideLegacy`, `BootOverrideUEFI`, `BootPState`, `BootRetry`, `BootType`, `BootTypeOrder0`, `BootTypeOrder1`, `BootTypeOrder2`, `BootTypeOrder2D`, `BootTypeOrder3`, `C6Enable`, `CAMargin`, `CKEIdleTimer`, `CKEProgramming`, `COMBaseAddress`, `CRAfterPost`, `CREnable`, `CRInfoWaitTime`, `CdnSupport`, `ChannelInterleaving`, `ChannelInterleaving_3Way`, `CheckCPUBIST`, `CkeIdleTimer`, `CkeProgramming`, `ClkGenSpreadSpectrumCheck`, `CoherencySupport`, `ColdBootFastSupport`, `ComBaseAddr`, `CompletionTimeout0`, `CompletionTimeout1`, `CompletionTimeout2`, `CompletionTimeout3`, `CompletionTimeout4`, `CompletionTimeout5`, `CompletionTimeout6`, `CompletionTimeout7`, `CompletionTimeoutValue0`, `CompletionTimeoutValue1`, `CompletionTimeoutValue2`, `CompletionTimeoutValue3`, `CompletionTimeoutValue4`, `CompletionTimeoutValue5`, `CompletionTimeoutValue6`, `CompletionTimeoutValue7`, `ConfigTDPLevel`, `ConfigTdpLock`, `CurrentUnderReport`, `CustomPowerPolicy`, `CustomRefreshRate`, `CustomRefreshRateEn`, `CustomizedFeatures`, `DCUIPPrefetcherEnable`, `DCUModeSelection`, `DCUStreamerPrefetcherEnable`, `DDRDebugLevel`, `DDRFreqLimit`, `DcpmmAveragePowerLimit`, `DcpmmEccModeSwitch`, `DcpmmMbbFeature`, `DcpmmMbbMaxPowerLimit`, `DdRefreshSupport`, `DdrFreqLimit`, `Degrade4SPreference`, `DemandScrubMode`, `DieInterleaving`, `DirectoryModeEn`, `DisableDirForAppDirect`, `DisplayMode`, `DramRaplEnable`, `DramRaplInit`, `EETurboDisable`, `EMCACSMIEn`, `EMCAEn`, `EadrSupport`, `EliminateDirectoryInFarMemory`, `EmcaCsmiEn`, `EmcaEn`, `EnableBIOSSSARMT`, `EnableBIOSSSARMTonFCB`, `EnableBiosSsaRMT`, `EnableBiosSsaRMTonFCB`, `EnableClockSpreadSpec`, `EnableProcHot`, `EnableThermalMonitor`, `EnableXE`, `EnableXe`, `EnforcePOR`, `ExecuteDisableBit`, `ExtendedType17`, `FDMSupport`, `FPKPortConfig0`, `FPKPortConfig1`, `FPKPortConfig2`, `FPKPortConfig3`, `FastGoConfig`, `FlowControl`, `FreqSelect`, `FrontPanelLock`, `GlobalBaudRate`, `GlobalDataBits`, `GlobalFlowControl`, `GlobalParity`, `GlobalStopBits`, `GlobalTerminalType`, `HWMemTest`, `IIOErrRegistersClearEn`, `IIOErrorEn`, `IMCInterleaving`, `IOAPICMode`, `IRQThreshold`, `ISOCEn`, `IioErrorPin0En`, `IioOOBMode`, `IntelSpeedSelectSupport`, `Interleave`, `InterruptRemap`, `Ipv4Pxe`, `Irq`, `IrqThreshold`, `IsocEn`, `KTIFailoverSMIEn`, `KTIPrefetchEn`, `KtiLinkL0pEn`, `KtiLinkL1En`, `KtiPrefetchEn`, `L2RfoPrefetchDisable`, `LLCDeadLineAlloc`, `LLCPrefetchEnable`, `LatchSystemShutdownState`, `LeakyBktHi`, `LeakyBktLo`, `LlcPrefetchEnable`, `LowOccupyControl`, `LpAsrMode`, `LsxImplementation`, `MCTPEn`, `MLCSpatialPrefetcherEnable`, `MLCStreamerPrefetcherEnable`, `MemCeFloodPolicy`, `MemInterleaveGran1LM`, `MemTestOnFastBoot`, `MemhotOutputOnlyOpt`, `MemhotSupport`, `MirrorMode`, `MlcSpatialPrefetcherEnable`, `MlcStreamerPrefetcherEnable`, `MmiohBase`, `MmiohSize`, `MonitorMWait`, `MonitorMwaitEnable`, `MultiSparingRanks`, `NetworkHttpsProtocol`, `NetworkProtocol`, `NgnArsOnBoot`, `NgnArsPublish`, `NgnAveragePower`, `NgnCmdTime`, `NgnEccRdChk`, `NgnThrottleTemp`, `NoBootReset`, `NumaEn`, `NvmQos`, `NvmdimmPerfConfig`, `NvmdimmPowerCyclePolicy`, `OSCx`, `OSWDTAction`, `OSWDTEnable`, `OSWDTTimeout`, `OemSecureBoot`, `OemTpmEnable`, `OnDieThermalThrottling`, `OsNativeAerSupport`, `OverclockingLock`, `PCHADREn`, `PCHPCIeGlobalASPM`, `PCHPCIeUX16MaxPayloadSize`, `PCHPCIeUX8MaxPayloadSize`, `PCHSATA`, `PCHSSATA`, `PCHUSBHSPort0`, `PCHUSBHSPort1`, `PCHUSBHSPort10`, `PCHUSBHSPort11`, `PCHUSBHSPort12`, `PCHUSBHSPort13`, `PCHUSBHSPort2`, `PCHUSBHSPort3`, `PCHUSBHSPort7`, `PCHUSBHSPort8`, `PCHUSBHSPort9`, `PCHUSBPerPortCtl`, `PCHUSBSSPort0`, `PCHUSBSSPort1`, `PCHUSBSSPort2`, `PCHUSBSSPort3`, `PCHUSBSSPort4`, `PCHUSBSSPort5`, `PCHUSBSSPort6`, `PCHUSBSSPort7`, `PCHUSBSSPort8`, `PCHUSBSSPort9`, `PCI64BitResourceAllocation`, `PCIeARISupport`, `PCIeGlobalASPM`, `PCIeLinkDis1`, `PCIeLinkDis10`, `PCIeLinkDis101`, `PCIeLinkDis105`, `PCIeLinkDis106`, `PCIeLinkDis107`, `PCIeLinkDis108`, `PCIeLinkDis109`, `PCIeLinkDis11`, `PCIeLinkDis110`, `PCIeLinkDis111`, `PCIeLinkDis112`, `PCIeLinkDis113`, `PCIeLinkDis114`, `PCIeLinkDis115`, `PCIeLinkDis116`, `PCIeLinkDis117`, `PCIeLinkDis118`, `PCIeLinkDis12`, `PCIeLinkDis122`, `PCIeLinkDis126`, `PCIeLinkDis127`, `PCIeLinkDis128`, `PCIeLinkDis129`, `PCIeLinkDis13`, `PCIeLinkDis130`, `PCIeLinkDis131`, `PCIeLinkDis132`, `PCIeLinkDis133`, `PCIeLinkDis134`, `PCIeLinkDis135`, `PCIeLinkDis136`, `PCIeLinkDis137`, `PCIeLinkDis138`, `PCIeLinkDis139`, `PCIeLinkDis143`, `PCIeLinkDis147`, `PCIeLinkDis148`, `PCIeLinkDis149`, `PCIeLinkDis150`, `PCIeLinkDis151`, `PCIeLinkDis152`, `PCIeLinkDis153`, `PCIeLinkDis154`, `PCIeLinkDis155`, `PCIeLinkDis156`, `PCIeLinkDis157`, `PCIeLinkDis158`, `PCIeLinkDis159`, `PCIeLinkDis160`, `PCIeLinkDis164`, `PCIeLinkDis17`, `PCIeLinkDis2`, `PCIeLinkDis21`, `PCIeLinkDis22`, `PCIeLinkDis23`, `PCIeLinkDis24`, `PCIeLinkDis25`, `PCIeLinkDis26`, `PCIeLinkDis27`, `PCIeLinkDis28`, `PCIeLinkDis29`, `PCIeLinkDis3`, `PCIeLinkDis30`, `PCIeLinkDis31`, `PCIeLinkDis32`, `PCIeLinkDis33`, `PCIeLinkDis34`, `PCIeLinkDis38`, `PCIeLinkDis4`, `PCIeLinkDis42`, `PCIeLinkDis43`, `PCIeLinkDis44`, `PCIeLinkDis45`, `PCIeLinkDis46`, `PCIeLinkDis47`, `PCIeLinkDis48`, `PCIeLinkDis49`, `PCIeLinkDis5`, `PCIeLinkDis50`, `PCIeLinkDis51`, `PCIeLinkDis52`, `PCIeLinkDis53`, `PCIeLinkDis54`, `PCIeLinkDis55`, `PCIeLinkDis59`, `PCIeLinkDis6`, `PCIeLinkDis63`, `PCIeLinkDis64`, `PCIeLinkDis65`, `PCIeLinkDis66`, `PCIeLinkDis67`, `PCIeLinkDis68`, `PCIeLinkDis69`, `PCIeLinkDis7`, `PCIeLinkDis70`, `PCIeLinkDis71`, `PCIeLinkDis72`, `PCIeLinkDis73`, `PCIeLinkDis74`, `PCIeLinkDis75`, `PCIeLinkDis76`, `PCIeLinkDis8`, `PCIeLinkDis80`, `PCIeLinkDis84`, `PCIeLinkDis85`, `PCIeLinkDis86`, `PCIeLinkDis87`, `PCIeLinkDis88`, `PCIeLinkDis89`, `PCIeLinkDis9`, `PCIeLinkDis90`, `PCIeLinkDis91`, `PCIeLinkDis92`, `PCIeLinkDis93`, `PCIeLinkDis94`, `PCIeLinkDis95`, `PCIeLinkDis96`, `PCIeLinkDis97`, `PCIePortDisable1`, `PCIePortDisable10`, `PCIePortDisable101`, `PCIePortDisable105`, `PCIePortDisable106`, `PCIePortDisable107`, `PCIePortDisable108`, `PCIePortDisable109`, `PCIePortDisable11`, `PCIePortDisable110`, `PCIePortDisable111`, `PCIePortDisable112`, `PCIePortDisable113`, `PCIePortDisable114`, `PCIePortDisable115`, `PCIePortDisable116`, `PCIePortDisable117`, `PCIePortDisable118`, `PCIePortDisable12`, `PCIePortDisable122`, `PCIePortDisable126`, `PCIePortDisable127`, `PCIePortDisable128`, `PCIePortDisable129`, `PCIePortDisable13`, `PCIePortDisable130`, `PCIePortDisable131`, `PCIePortDisable132`, `PCIePortDisable133`, `PCIePortDisable134`, `PCIePortDisable135`, `PCIePortDisable136`, `PCIePortDisable137`, `PCIePortDisable138`, `PCIePortDisable139`, `PCIePortDisable143`, `PCIePortDisable147`, `PCIePortDisable148`, `PCIePortDisable149`, `PCIePortDisable150`, `PCIePortDisable151`, `PCIePortDisable152`, `PCIePortDisable153`, `PCIePortDisable154`, `PCIePortDisable155`, `PCIePortDisable156`, `PCIePortDisable157`, `PCIePortDisable158`, `PCIePortDisable159`, `PCIePortDisable160`, `PCIePortDisable164`, `PCIePortDisable17`, `PCIePortDisable2`, `PCIePortDisable21`, `PCIePortDisable22`, `PCIePortDisable23`, `PCIePortDisable24`, `PCIePortDisable25`, `PCIePortDisable26`, `PCIePortDisable27`, `PCIePortDisable28`, `PCIePortDisable29`, `PCIePortDisable3`, `PCIePortDisable30`, `PCIePortDisable31`, `PCIePortDisable32`, `PCIePortDisable33`, `PCIePortDisable34`, `PCIePortDisable38`, `PCIePortDisable4`, `PCIePortDisable42`, `PCIePortDisable43`, `PCIePortDisable44`, `PCIePortDisable45`, `PCIePortDisable46`, `PCIePortDisable47`, `PCIePortDisable48`, `PCIePortDisable49`, `PCIePortDisable5`, `PCIePortDisable50`, `PCIePortDisable51`, `PCIePortDisable52`, `PCIePortDisable53`, `PCIePortDisable54`, `PCIePortDisable55`, `PCIePortDisable59`, `PCIePortDisable6`, `PCIePortDisable63`, `PCIePortDisable64`, `PCIePortDisable65`, `PCIePortDisable66`, `PCIePortDisable67`, `PCIePortDisable68`, `PCIePortDisable69`, `PCIePortDisable7`, `PCIePortDisable70`, `PCIePortDisable71`, `PCIePortDisable72`, `PCIePortDisable73`, `PCIePortDisable74`, `PCIePortDisable75`, `PCIePortDisable76`, `PCIePortDisable8`, `PCIePortDisable80`, `PCIePortDisable84`, `PCIePortDisable85`, `PCIePortDisable86`, `PCIePortDisable87`, `PCIePortDisable88`, `PCIePortDisable89`, `PCIePortDisable9`, `PCIePortDisable90`, `PCIePortDisable91`, `PCIePortDisable92`, `PCIePortDisable93`, `PCIePortDisable94`, `PCIePortDisable95`, `PCIePortDisable96`, `PCIePortDisable97`, `PCIePortLinkSpeed1`, `PCIePortLinkSpeed10`, `PCIePortLinkSpeed101`, `PCIePortLinkSpeed105`, `PCIePortLinkSpeed106`, `PCIePortLinkSpeed107`, `PCIePortLinkSpeed108`, `PCIePortLinkSpeed109`, `PCIePortLinkSpeed11`, `PCIePortLinkSpeed110`, `PCIePortLinkSpeed111`, `PCIePortLinkSpeed112`, `PCIePortLinkSpeed113`, `PCIePortLinkSpeed114`, `PCIePortLinkSpeed115`, `PCIePortLinkSpeed116`, `PCIePortLinkSpeed117`, `PCIePortLinkSpeed118`, `PCIePortLinkSpeed12`, `PCIePortLinkSpeed122`, `PCIePortLinkSpeed126`, `PCIePortLinkSpeed127`, `PCIePortLinkSpeed128`, `PCIePortLinkSpeed129`, `PCIePortLinkSpeed13`, `PCIePortLinkSpeed130`, `PCIePortLinkSpeed131`, `PCIePortLinkSpeed132`, `PCIePortLinkSpeed133`, `PCIePortLinkSpeed134`, `PCIePortLinkSpeed135`, `PCIePortLinkSpeed136`, `PCIePortLinkSpeed137`, `PCIePortLinkSpeed138`, `PCIePortLinkSpeed139`, `PCIePortLinkSpeed143`, `PCIePortLinkSpeed147`, `PCIePortLinkSpeed148`, `PCIePortLinkSpeed149`, `PCIePortLinkSpeed150`, `PCIePortLinkSpeed151`, `PCIePortLinkSpeed152`, `PCIePortLinkSpeed153`, `PCIePortLinkSpeed154`, `PCIePortLinkSpeed155`, `PCIePortLinkSpeed156`, `PCIePortLinkSpeed157`, `PCIePortLinkSpeed158`, `PCIePortLinkSpeed159`, `PCIePortLinkSpeed160`, `PCIePortLinkSpeed164`, `PCIePortLinkSpeed17`, `PCIePortLinkSpeed2`, `PCIePortLinkSpeed21`, `PCIePortLinkSpeed22`, `PCIePortLinkSpeed23`, `PCIePortLinkSpeed24`, `PCIePortLinkSpeed25`, `PCIePortLinkSpeed26`, `PCIePortLinkSpeed27`, `PCIePortLinkSpeed28`, `PCIePortLinkSpeed29`, `PCIePortLinkSpeed3`, `PCIePortLinkSpeed30`, `PCIePortLinkSpeed31`, `PCIePortLinkSpeed32`, `PCIePortLinkSpeed33`, `PCIePortLinkSpeed34`, `PCIePortLinkSpeed38`, `PCIePortLinkSpeed4`, `PCIePortLinkSpeed42`, `PCIePortLinkSpeed43`, `PCIePortLinkSpeed44`, `PCIePortLinkSpeed45`, `PCIePortLinkSpeed46`, `PCIePortLinkSpeed47`, `PCIePortLinkSpeed48`, `PCIePortLinkSpeed49`, `PCIePortLinkSpeed5`, `PCIePortLinkSpeed50`, `PCIePortLinkSpeed51`, `PCIePortLinkSpeed52`, `PCIePortLinkSpeed53`, `PCIePortLinkSpeed54`, `PCIePortLinkSpeed55`, `PCIePortLinkSpeed59`, `PCIePortLinkSpeed6`, `PCIePortLinkSpeed63`, `PCIePortLinkSpeed64`, `PCIePortLinkSpeed65`, `PCIePortLinkSpeed66`, `PCIePortLinkSpeed67`, `PCIePortLinkSpeed68`, `PCIePortLinkSpeed69`, `PCIePortLinkSpeed7`, `PCIePortLinkSpeed70`, `PCIePortLinkSpeed71`, `PCIePortLinkSpeed72`, `PCIePortLinkSpeed73`, `PCIePortLinkSpeed74`, `PCIePortLinkSpeed75`, `PCIePortLinkSpeed76`, `PCIePortLinkSpeed8`, `PCIePortLinkSpeed80`, `PCIePortLinkSpeed84`, `PCIePortLinkSpeed85`, `PCIePortLinkSpeed86`, `PCIePortLinkSpeed87`, `PCIePortLinkSpeed88`, `PCIePortLinkSpeed89`, `PCIePortLinkSpeed9`, `PCIePortLinkSpeed90`, `PCIePortLinkSpeed91`, `PCIePortLinkSpeed92`, `PCIePortLinkSpeed93`, `PCIePortLinkSpeed94`, `PCIePortLinkSpeed95`, `PCIePortLinkSpeed96`, `PCIePortLinkSpeed97`, `PCIeRootPortASPM0`, `PCIeRootPortASPM1`, `PCIeRootPortASPM10`, `PCIeRootPortASPM11`, `PCIeRootPortASPM12`, `PCIeRootPortASPM13`, `PCIeRootPortASPM14`, `PCIeRootPortASPM15`, `PCIeRootPortASPM16`, `PCIeRootPortASPM17`, `PCIeRootPortASPM18`, `PCIeRootPortASPM19`, `PCIeRootPortASPM2`, `PCIeRootPortASPM3`, `PCIeRootPortASPM6`, `PCIeRootPortASPM7`, `PCIeRootPortASPM8`, `PCIeRootPortASPM9`, `PCIeRootPortEn0`, `PCIeRootPortEn1`, `PCIeRootPortEn10`, `PCIeRootPortEn11`, `PCIeRootPortEn12`, `PCIeRootPortEn13`, `PCIeRootPortEn14`, `PCIeRootPortEn15`, `PCIeRootPortEn16`, `PCIeRootPortEn17`, `PCIeRootPortEn18`, `PCIeRootPortEn19`, `PCIeRootPortEn2`, `PCIeRootPortEn3`, `PCIeRootPortEn6`, `PCIeRootPortEn7`, `PCIeRootPortEn8`, `PCIeRootPortEn9`, `PCIeRootPortMSIE0`, `PCIeRootPortMSIE1`, `PCIeRootPortMSIE10`, `PCIeRootPortMSIE11`, `PCIeRootPortMSIE12`, `PCIeRootPortMSIE13`, `PCIeRootPortMSIE14`, `PCIeRootPortMSIE15`, `PCIeRootPortMSIE16`, `PCIeRootPortMSIE17`, `PCIeRootPortMSIE18`, `PCIeRootPortMSIE19`, `PCIeRootPortMSIE2`, `PCIeRootPortMSIE3`, `PCIeRootPortMSIE6`, `PCIeRootPortMSIE7`, `PCIeRootPortMSIE8`, `PCIeRootPortMSIE9`, `PCIeRootPortMaxPayLoadSize0`, `PCIeRootPortMaxPayLoadSize1`, `PCIeRootPortMaxPayLoadSize10`, `PCIeRootPortMaxPayLoadSize11`, `PCIeRootPortMaxPayLoadSize12`, `PCIeRootPortMaxPayLoadSize13`, `PCIeRootPortMaxPayLoadSize14`, `PCIeRootPortMaxPayLoadSize15`, `PCIeRootPortMaxPayLoadSize16`, `PCIeRootPortMaxPayLoadSize17`, `PCIeRootPortMaxPayLoadSize18`, `PCIeRootPortMaxPayLoadSize19`, `PCIeRootPortMaxPayLoadSize2`, `PCIeRootPortMaxPayLoadSize3`, `PCIeRootPortMaxPayLoadSize6`, `PCIeRootPortMaxPayLoadSize7`, `PCIeRootPortMaxPayLoadSize8`, `PCIeRootPortMaxPayLoadSize9`, `PCIeRootPortSpeed0`, `PCIeRootPortSpeed1`, `PCIeRootPortSpeed10`, `PCIeRootPortSpeed11`, `PCIeRootPortSpeed12`, `PCIeRootPortSpeed13`, `PCIeRootPortSpeed14`, `PCIeRootPortSpeed15`, `PCIeRootPortSpeed16`, `PCIeRootPortSpeed17`, `PCIeRootPortSpeed18`, `PCIeRootPortSpeed19`, `PCIeRootPortSpeed2`, `PCIeRootPortSpeed3`, `PCIeRootPortSpeed6`, `PCIeRootPortSpeed7`, `PCIeRootPortSpeed8`, `PCIeRootPortSpeed9`, `PCIeSRIOVSupport`, `PCIeTopology0`, `PCIeTopology1`, `PCIeTopology10`, `PCIeTopology11`, `PCIeTopology12`, `PCIeTopology13`, `PCIeTopology14`, `PCIeTopology15`, `PCIeTopology16`, `PCIeTopology17`, `PCIeTopology18`, `PCIeTopology19`, `PCIeTopology2`, `PCIeTopology3`, `PCIeTopology6`, `PCIeTopology7`, `PCIeTopology8`, `PCIeTopology9`, `POSTBootWDTimerPolicy`, `POSTBootWDTimerTimeout`, `PPDEn`, `PStateDomain`, `PXE1Setting`, `PXE2Setting`, `PXE3Setting`, `PXE4Setting`, `PXE5Setting`, `PXE6Setting`, `PXE7Setting`, `PXE8Setting`, `PXEBootToLan`, `PXEBootToLanLegacy`, `PXEBootToLanUEFI`, `PXEOnly`, `PackageCState`, `PagePolicy`, `PartialMirrorSAD0`, `PartialMirrorUefi`, `PartialMirrorUefiPercent`, `PassThroughDMA`, `PatrolScrub`, `PatrolScrubDuration`, `PchBackUsbPort1`, `PchBackUsbPort2`, `PchBackUsbPort3`, `PchBackUsbPort4`, `PchFrontUsbPort1`, `PchFrontUsbPort2`, `PchFrontUsbPort3`, `PchFrontUsbPort4`, `PchInternalUsbPort1`, `PchInternalUsbPort2`, `PchPcieUX16MaxPayloadSize`, `PchPcieUX8MaxPayloadSize`, `PchSata`, `PchUsbDegradeBar`, `PchsSata`, `Pci64BitResourceAllocation`, `PcieAerEcrcEn`, `PcieAerSurpriseLinkDownEn`, `PcieAerUreEn`, `PcieDmiAspm`, `PciePortPolicy`, `PcieRelaxedOrdering`, `PerformanceTuningMode`, `Persistent`, `PkgCLatNeg`, `PlusOneEn`, `PmemCaching`, `PoisonEn`, `PostedInterrupt`, `PowerOnPassword`, `PowerSaving`, `PpdEn`, `ProcessorActiveCore`, `ProcessorActivePbf`, `ProcessorAutonomousCStateEnable`, `ProcessorAutonomousCstateEnable`, `ProcessorC1eEnable`, `ProcessorConfigurePbf`, `ProcessorEISTEnable`, `ProcessorEISTPSDFunc`, `ProcessorEPPEnable`, `ProcessorEPPProfile`, `ProcessorEistEnable`, `ProcessorEistPsdFunc`, `ProcessorEppProfile`, `ProcessorFlexibleRatio`, `ProcessorFlexibleRatioOverrideEnable`, `ProcessorHWPMEnable`, `ProcessorHWPMInterrupt`, `ProcessorHyperThreading`, `ProcessorHyperThreadingDisable`, `ProcessorLTSXEnable`, `ProcessorLtsxEnable`, `ProcessorOutofBandAlternateEPB`, `ProcessorRaplPrioritization`, `ProcessorSPD`, `ProcessorSinglePCTLEn`, `ProcessorVMXEnable`, `ProcessorVmxEnable`, `ProcessorX2APIC`, `ProcessorX2apic`, `ProchotResponseRatio`, `PwrPerfTuning`, `PxeBootToLan`, `PxeRetryCount`, `PxeRetrylimites`, `PxeTimeoutRetryControl`, `QpiLinkSpeed`, `QuickBoot`, `QuietBoot`, `RMTOnColdFastBoot`, `RMTPatternLength`, `RankInterleaving`, `RankMargin`, `RankSparing`, `RdtCatOpportunisticTuning`, `ResetAndEraseToAllNVDimm`, `RestoreNVDIMMS`, `Rrq`, `SATAAlternateID`, `SATAExternal0`, `SATAExternal1`, `SATAExternal2`, `SATAExternal3`, `SATAExternal4`, `SATAExternal5`, `SATAExternal6`, `SATAExternal7`, `SATAHotPlug0`, `SATAHotPlug1`, `SATAHotPlug2`, `SATAHotPlug3`, `SATAHotPlug4`, `SATAHotPlug5`, `SATAHotPlug6`, `SATAHotPlug7`, `SATAInterfaceMode`, `SATAPort0`, `SATAPort1`, `SATAPort2`, `SATAPort3`, `SATAPort4`, `SATAPort5`, `SATAPort6`, `SATAPort7`, `SATARAIDLoadEFIDriver`, `SATATopology0`, `SATATopology1`, `SATATopology2`, `SATATopology3`, `SATATopology4`, `SATATopology5`, `SATATopology6`, `SATATopology7`, `SATAType0`, `SATAType1`, `SATAType2`, `SATAType3`, `SATAType4`, `SATAType5`, `SATAType6`, `SATAType7`, `SNCEn`, `SPBoot`, `SSATAAlternateID`, `SSATAExternal0`, `SSATAExternal1`, `SSATAExternal2`, `SSATAExternal3`, `SSATAExternal4`, `SSATAExternal5`, `SSATAHotPlug0`, `SSATAHotPlug1`, `SSATAHotPlug2`, `SSATAHotPlug3`, `SSATAHotPlug4`, `SSATAHotPlug5`, `SSATAInterfaceMode`, `SSATAPort0`, `SSATAPort1`, `SSATAPort2`, `SSATAPort3`, `SSATAPort4`, `SSATAPort5`, `SSATARAIDLoadEFIDriver`, `SSATATopology0`, `SSATATopology1`, `SSATATopology2`, `SSATATopology3`, `SSATATopology4`, `SSATATopology5`, `SSATAType0`, `SSATAType1`, `SSATAType2`, `SSATAType3`, `SSATAType4`, `SSATAType5`, `SataInterfaceMode`, `SecureBoot`, `SerialDebugMsgLvl`, `SimplePassWord`, `Slot1PXESetting`, `Slot2PXESetting`, `Slot3PXESetting`, `Slot4PXESetting`, `Slot5PXESetting`, `Slot6PXESetting`, `Slot7PXESetting`, `Slot8PXESetting`, `SlotPxeDis`, `SlotPxeEnable`, `SncEn`, `SocketInterleaveBelow4GB`, `SpareErrTh`, `SpdDataRepair`, `SpsAltitude`, `SriovEnablePolicy`, `StaleAtoSOptEn`, `StaticTurbo`, `Support40Bit`, `Support44Bit`, `SupportOSCtrlAER`, `SysDBGLevel`, `SystemCpuUsage`, `SystemErrorEn`, `SystemPcieGlobalAspm`, `SystemVMDConfigEnable`, `TCCActivationOffset`, `TStateEnable`, `TcoTimeout`, `Thermalmemtrip`, `Thermalthrottlingsupport`, `TpmAvailability`, `TurboMode`, `TurboPowerLimitLock`, `TurboRatioLimitCores0`, `TurboRatioLimitCores1`, `TurboRatioLimitCores2`, `TurboRatioLimitCores3`, `TurboRatioLimitCores4`, `TurboRatioLimitCores5`, `TurboRatioLimitCores6`, `TurboRatioLimitCores7`, `TurboRatioLimitRatio0`, `TurboRatioLimitRatio1`, `TurboRatioLimitRatio2`, `TurboRatioLimitRatio3`, `TurboRatioLimitRatio4`, `TurboRatioLimitRatio5`, `TurboRatioLimitRatio6`, `TurboRatioLimitRatio7`, `UFSDisable`, `USBBoot`, `USBPrecondition`, `UefiPXE1Setting`, `UefiPXE2Setting`, `UefiPXE3Setting`, `UefiPXE4Setting`, `VMDConfigEnable`, `VTdSupport`, `VideoSelect`, `WHEALogMemoryEn`, `WHEALogPCIEn`, `WHEALogProcEn`, `WHEASupportEn`, `WakeOnPME`, `WakeOnS5`, `WakeOnS5DayOfMonth`, `WarmBootFastSupport`, `WheaLogMemoryEn`, `WheaLogPciEn`, `WheaLogProcEn`, `WheaSupportEn`, `XHCIDisMSICapability`, `XHCIOCMapEnabled`, `XHCIWakeOnUsbEnabled`, `XPTPrefetchEn`, `XptPrefetchEn`, `leakyBktHour`, `leakyBktMinute`, `partialmirrorsad0`, `refreshMode`, `sSataInterfaceMode`, `serialDebugMsgLvl`, `spareErrTh`, `thermalthrottlingsupport`, `volMemMode` |

### 4.10.2.2 修改账户策略（差异 75）

- BMC section: `3.6.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/AccountService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| body | `CertificateOverdueWarningTime`, `Huawei` | `AccessRole`, `CLISessionTimeoutMinutes`, `CrlVerificationEnabled`, `EmergencyLoginUser`, `Enabled`, `HuaweiPublic`, `InterChassisAuthentication`, `LocalAccountAuth`, `LocalRole`, `OSAdministratorPrivilegeEnabled`, `OSUserManagementEnabled`, `PasswordExpirationDays`, `PasswordPattern`, `PasswordRulePolicy`, `RemoteGroup`, `RemoteRoleMapping`, `RequireChangePasswordAction`, `SSHPasswordAuthenticationEnabled`, `SystemLockDownEnabled`, `TwoFactorAuthenticationInformation`, `UsernamePasswordCompareEnabled`, `UsernamePasswordCompareInfo`, `UsernamePasswordCompareLength` |
| response | `Huawei`, `Oem` | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `Certificates`, `CrlValidFrom`, `CrlValidTo`, `EmergencyLoginUser`, `Enabled`, `HTTPBasicAuth`, `InitialAccountPrivilegeRestrictEnabled`, `InterChassisAuthentication`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KerberosService`, `KeyUsage`, `LdapService`, `LocalAccountAuth`, `LocalRole`, `OSUserManagementEnabled`, `PasswordExpirationDays`, `PasswordPattern`, `PasswordRulePolicy`, `PublicKeyLengthBits`, `RemoteGroup`, `RemoteRoleMapping`, `RequireChangePasswordAction`, `RootCertificate`, `SSHPasswordAuthenticationEnabled`, `SerialNumber`, `SignatureAlgorithm`, `Status`, `SystemLockDownEnabled`, `TwoFactorAuthenticationInformation`, `UsernamePasswordCompareEnabled`, `UsernamePasswordCompareInfo`, `UsernamePasswordCompareLength`, `ValidFrom`, `ValidTo`, `target` |

### 4.4.2 查询指定机柜资源信息（差异 74）

- BMC section: `3.4.2`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Assembly`, `Cabinet`, `CabinetSerialNumbe`, `ComputerSystems/ManagedBy/Processors`, `InterconType`, `LeakDetectors`, `LedGroup`, `ManagedBy`, `NPUBootOption`, `NPUNum`, `Oem/Huawei`, `Power`, `PresentDPUCount`, `Sensors`, `Switches`, `Thermal`, `ThermalSubsystem`, `Units` | `AssetOwner`, `AvailableRackSpaceU`, `BackupBatteryUnits`, `BasicRackSN`, `Board`, `Building`, `BunchId`, `BunchType`, `CabinetSerialNumber`, `Chassis`, `ChassisLocation`, `CheckInTime`, `City`, `ContainedBy`, `Country`, `DepthMm`, `DeviceType`, `Direction`, `DirectionType`, `DiscoveredTime`, `EmptyRackSN`, `ExtendField`, `Floor`, `HeightMm`, `HouseNumber`, `IndicatorColor`, `InfoFormat`, `LifeCycleYear`, `LoadCapacityKg`, `ManufacturingDate`, `MezzCardNum`, `Placement`, `PostalAddress`, `PostalCode`, `Presence`, `Processors`, `ProductName`, `RFIDTagUID`, `RWCapability`, `Rack`, `RackModel`, `RatedPowerWatts`, `Room`, `Row`, `SDCardNum`, `SDContollerNum`, `Street`, `Territory`, `TopUSlot`, `TotalUCount`, `Type`, `UHeight`, `UcountUsed`, `UnitOccupyDirection`, `WeightKg`, `WidthMm` |

### 4.2.46 查询SP服务的配置结果资源（差异 55）

- BMC section: `3.2.84`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPResult/{result_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Aborted`, `ActualTestResult`, `AssetVerification`, `CPUID`, `CPU详细信息`, `Cancelled`, `Cancelling`, `Capacity`, `ClockSpeed`, `Completed`, `CountItem`, `CountVerification`, `DeviceName`, `DiagnoseMessage`, `DiagnoseResult`, `Diagnosing`, `DignoseResult`, `Executing`, `ExpectedTestResult`, `Failed`, `Finished`, `Firmware`, `Interrupted`, `MaxPower`, `Metrics`, `NPU详细信息`, `PartNumber`, `Pending`, `Position`, `Power详细信息`, `Qty`, `Reason`, `Reasons`, `RebootDelayMinutes`, `Result`, `ResultRaw`, `Running`, `Stopping`, `Successful`, `Suggestion`, `TaskList`, `TaskName`, `TaskState任务状态说明`, `Threshold`, `Type`, `Value`, `Waiting`, `decrypt_failed`, `encrypt_failed`, `network_failed`, `process_failed`, `progressing`, `successful`, `trans_failed`, `upload_failed` |

### 4.2.22 修改安全服务集合资源信息（差异 54）

- BMC section: `3.2.49`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SecurityService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| body | — | `CipherSuite1`, `CipherSuite17`, `CipherSuite2`, `CipherSuite3`, `ComponentMeasurementPolicy`, `DHE-RSA-AES128-GCM-SHA256Enabled`, `DHE-RSA-AES256-GCM-SHA384Enabled`, `ECDHE-ECDSA-AES128-GCM-SHA256Enabled`, `ECDHE-ECDSA-AES256-GCM-SHA384Enabled`, `ECDHE-RSA-AES128-GCM-SHA256Enabled`, `ECDHE-RSA-AES256-GCM-SHA384Enabled`, `Enabled`, `HttpsTransferCertVerification`, `IPMBAccessRole`, `IPMIChannelAccess`, `MasterKeyUpdateInterval`, `RMCPCipherSuites`, `SMSAccessRole`, `SOLAutoOSLockEnabled`, `SOLAutoOSLockKey`, `SSHCiphers`, `SSHHostKeyAlgorithms`, `SSHKexAlgorithms`, `SSHMACs`, `SSLCipherSuites`, `aes128-ctrEnabled`, `aes128-gcm@openssh.comEnabled`, `aes192-ctrEnabled`, `aes256-ctrEnabled`, `aes256-gcm@openssh.comEnabled`, `chacha20-poly1305@openssh.comEnabled`, `curve25519-sha256@libssh.orgEnabled`, `curve25519-sha256Enabled`, `diffie-hellman-group-exchange-sha1Enabled`, `diffie-hellman-group-exchange-sha256Enabled`, `diffie-hellman-group14-sha1Enabled`, `diffie-hellman-group16-sha512Enabled`, `diffie-hellman-group18-sha512Enabled`, `ecdsa-sha2-nistp256Enabled`, `ecdsa-sha2-nistp384Enabled`, `ecdsa-sha2-nistp521Enabled`, `hmac-sha2-256-etm@openssh.comEnabled`, `hmac-sha2-256Enabled`, `hmac-sha2-512-etm@openssh.comEnabled`, `hmac-sha2-512Enabled`, `rsa-sha2-256Enabled`, `rsa-sha2-512Enabled`, `ssh-ed25519-cert-v01@openssh.comEnabled`, `ssh-ed25519Enabled`, `ssh-rsa-cert-v01@openssh.comEnabled`, `ssh-rsaEnabled` |
| response | — | `ComponentMeasurementPolicy` |

### 4.7.7 创建事件订阅资源（差异 54）

- BMC section: `3.9.7`  method: `POST`
- PoDM URI: `/redfish/v1/EventService/Subscriptions`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `AuthenticationKey`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionProtocol`, `EventFormatType`, `HuaweiPublic`, `MetricReportDefinitions`, `Oem`, `OriginResources`, `SNMP`, `ServerIdentity`, `Severities`, `SubscriptionType`, `TrapCommunity`, `TrapMode` |
| response | `Message`, `MessageArgs`, `MessageId`, `Resolution`, `Severity`, `code`, `message` | `@Redfish.ActionInfo`, `@odata.context`, `@odata.id`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `Context`, `DeliveryRetryPolicy`, `Destination`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `EventTypes`, `HttpHeaders`, `Id`, `MessageIds`, `Name`, `OriginResources`, `Protocol`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |

### 4.2.20 修改指定PoDManager网卡信息（差异 53）

- BMC section: `3.2.43`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/EthernetInterfaces/{ethernetinterface_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `ifmatch_value` | `If-Match` |
| body | `ManagementNetworkPorts`, `PortNumber`, `VLANEnable`, `VLANId` | `AdaptivePort`, `ChassisLanSubNet`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `DNSAddressOrigin`, `FQDN`, `HostName`, `HuaweiPublic`, `IPVersion`, `IPv4Addresses`, `IPv6Addresses`, `IPv6DefaultGateway`, `IPv6Enabled`, `IPv6StaticAddresses`, `ManagementNetworkPort`, `ManagementNetworkPortMembers`, `NameServers`, `NetworkPortMode`, `Oem`, `OperatingMode`, `StaticNameServers`, `UseNTPServers`, `VLAN` |
| response | `ManagementNetworkPorts`, `ManagementNetworkPorts@Redfish.AllowableValues`, `Oem/Huawei` | `AdaptiveFlag`, `AdaptivePort`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link`, `ManagementNetworkPort`, `ManagementNetworkPort@Redfish.AllowableValues`, `ManagementNetworkPortMembers`, `NetworkPortMode`, `OperatingMode`, `SpeedMbps`, `StaticNameServers`, `SwitchConnectionPortIDs`, `SwitchConnections`, `SwitchManagementIP`, `UseNTPServers`, `VLAN` |

### 4.10.2.1 查询账户策略（差异 53）

- BMC section: `3.6.1`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `Huawei`, `Oem` | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `CertificateRevocationCheckEnabled`, `Certificates`, `CrlValidFrom`, `CrlValidTo`, `CrlVerificationEnabled`, `EmergencyLoginUser`, `Enabled`, `HTTPBasicAuth`, `InterChassisAuthentication`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KerberosService`, `KeyUsage`, `LdapService`, `LocalAccountAuth`, `LocalRole`, `OSAdministratorPrivilegeEnabled`, `OSUserManagementEnabled`, `PasswordExpirationDays`, `PasswordPattern`, `PasswordRulePolicy`, `PublicKeyLengthBits`, `RemoteGroup`, `RemoteRoleMapping`, `RequireChangePasswordAction`, `RootCertificate`, `SSHPasswordAuthenticationEnabled`, `SerialNumber`, `SignatureAlgorithm`, `Status`, `SystemLockDownEnabled`, `TwoFactorAuthenticationInformation`, `TwoFactorAuthenticationStateEnabled`, `UsernamePasswordCompareEnabled`, `UsernamePasswordCompareInfo`, `UsernamePasswordCompareLength`, `ValidFrom`, `ValidTo`, `target` |

### 4.3.45 修改BIOS设置资源属性（差异 52）

- BMC section: `3.3.37`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios/Settings`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `ATS`, `BMCWDTEnable`, `BootPState`, `BootTypeOrder0`, `BootTypeOrder1`, `BootTypeOrder2`, `BootTypeOrder3`, `C6Enable`, `CREnable`, `CoherencySupport`, `CustomPowerPolicy`, `DCUIPPrefetcherEnable`, `DCUStreamerPrefetcherEnable`, `DDRFreqLimit`, `EnableXE`, `FPKPortConfig0`, `FPKPortConfig1`, `FPKPortConfig2`, `FPKPortConfig3`, `GlobalBaudRate`, `InterruptRemap`, `KtiLinkL0pEn`, `KtiLinkL1En`, `MLCSpatialPrefetcherEnable`, `MLCStreamerPrefetcherEnable`, `MonitorMwaitEnable`, `NumaEn`, `OSWDTEnable`, `PCIePortDisable1`, `PCIePortDisable8`, `PCIePortDisable85`, `PCIeSRIOVSupport`, `PStateDomain`, `PXEBootToLanLegacy`, `PXEBootToLanUEFI`, `PassThroughDMA`, `PatrolScrub`, `PowerSaving`, `ProcessorC1eEnable`, `ProcessorEISTEnable`, `ProcessorFlexibleRatioOverrideEnable`, `ProcessorHWPMEnable`, `ProcessorHyperThreadingDisable`, `ProcessorX2APIC`, `PxeTimeoutRetryControl`, `QpiLinkSpeed`, `QuickBoot`, `QuietBoot`, `TStateEnable`, `VTdSupport` |
| response | `Oem/Huawei/Public` | `BIOS设置资源信息` |

### 4.4.3 修改指定机柜资源信息（差异 50）

- BMC section: `3.4.3`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `ChassisID`, `InterconType`, `SuperPodEnabled` | `AssetTag`, `HuaweiPublic`, `IsUBControlNode`, `IsUBFabricMode`, `LocationIndicatorActive`, `Oem`, `SSDMediaLifeLeftPercentThreshold`, `ServerIndex`, `TopologyType` |
| response | `Assembly`, `Cabinet`, `CabinetSerialNumbe`, `ComputerSystems/ManagedBy/Processors`, `DeviceSlotID`, `EnclosureSerialNumber`, `HeadNodeId`, `Info`, `InterconType`, `IsUBControlNode`, `IsUBFabricMode`, `LeakDetectors`, `LedGroup`, `Location`, `ManagedBy`, `MaxPowerWatts`, `MinPowerWatts`, `Oem/Huawei`, `Power`, `Sensors`, `Switches`, `Thermal`, `ThermalSubsystem`, `TrustedComponents`, `TypicalConfigurationRackSN`, `UBMDeployMode`, `Units` | `BackupBatteryUnits`, `Board`, `Chassis`, `ChassisLocation`, `ManufacturingDate`, `MezzCardNum`, `Presence`, `ProductName`, `SDCardNum`, `SDContollerNum`, `Type` |

### 4.3.3 修改指定系统资源属性（差异 42）

- BMC section: `3.3.3`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `IP`, `number`, `power_control` | `AutoOSLockEnabled`, `AutoOSLockKey`, `AutoOSLockType`, `BiosDynamicParamConfig`, `Boot`, `BootSourceOverrideEnabled`, `BootSourceOverrideMode`, `BootSourceOverrideTarget`, `BootupSequence`, `CPUPowerAdjustment`, `CPUThresholdPercent`, `DelaySecondsAfterCpuThermalTrip`, `DisableKeyboardDuringBiosStartup`, `GraphicalConsole`, `HardDiskThresholdPercent`, `HuaweiPublic`, `KVMSettings`, `LeakStrategy`, `MemoryThresholdPercent`, `NpuAbility`, `Oem`, `PersistentUSBConnectionEnabled`, `Port`, `PowerMode`, `PowerOnAfterCpuThermalTrip`, `PowerRestoreDelayMode`, `SSDMediaLifeLeftPercentThreshold`, `ServiceEnabled`, `VirtualMediaConfig`, `VncSettings` |
| response | `NpuAbility`, `Oem/Huawei/Public`, `PostState`, `Type`, `Value` | `DelaySecondsAfterCpuThermalTrip`, `PowerMode`, `PowerOnAfterCpuThermalTrip`, `SSDMediaLifeLeftPercentThreshold` |

### 4.4.7 修改指定机柜散热资源信息（差异 40）

- BMC section: `3.4.8`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Thermal`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `DA122Cv2`, `FanSpeedPercents`, `PAC1220V6`, `PangeaV6_Arctic`, `PangeaV6_Atlantic`, `PangeaV6_Pacific`, `S920S00`, `S920S00K`, `S920S10`, `S920S10K`, `S920X00`, `S920X00K`, `S920X01`, `S920X01K`, `S920X02`, `S920X03`, `S920X05`, `S920X05K`, `S920X10`, `S920X10K`, `TS200-1280`, `TS200-2180`, `TS200-2180K`, `TS200-2280`, `TS200-2280E`, `TS200-2280K`, `TS200-2480`, `TS200-2480K`, `TS200-5180`, `TS200-5280`, `TS200-5280K`, `TS200-5290`, `TemperatureRangeCelsius`, `X6800` | `FanSpeedCustom`, `HuaweiPublic`, `InletTemperature`, `Oem` |
| response | `ModelPredictiveControlEnabled`, `Oem/Huawei` | — |

### 4.2.64 修改诊断服务资源（差异 38）

- BMC section: `3.2.101`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| body | — | `DeteriorationPredictionEnabled`, `DiskSubhealthFunction`, `DrivesLogCollectEnable`, `DrivesLogCollectInterval`, `LifespanEstimateAlarmEnabled`, `LifespanEstimateEnabled`, `OpticalModuleSubhealthFunction` |
| response | `@odata.context`, `@odata.id`, `@odata.type`, `Actions`, `BlackBoxDumpEnabled`, `BlackBoxEnabled`, `BlackBoxSize`, `CreateTime`, `DfpServiceEnabled`, `DiagnosticService.CaptureScreenShot`, `DiagnosticService.DeleteScreenShot`, `DiagnosticService.ExportBlackBox`, `DiagnosticService.ExportNPULog`, `DiagnosticService.ExportSerialPortData`, `DiagnosticService.ExportVideo`, `DiagnosticService.StopVideoPlayback`, `Id`, `Name`, `Oem/Huawei`, `PCIeInterfaceEnabled`, `ScreenShotCreateTime`, `ScreenShotEnabled`, `SerialPortDataEnabled`, `SerialPortDataSize`, `VideoPlaybackConnNum`, `VideoRecordInfo`, `VideoRecordingEnabled`, `VideoSizeByte`, `WorkRecord` | — |

### 4.2.17 修改PoDManager服务信息（差异 33）

- BMC section: `3.2.45`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/NetworkProtocol`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `ifmatch_value` | `If-Match` |
| body | `Huawei` | `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `HttpProtocolVersion`, `HuaweiPublic`, `IPMI`, `NTPServers`, `NotifyEnabled`, `Port1`, `Port2`, `RMCPEnabled`, `RMCPPlusEnabled`, `SSDP` |
| response | `HTTP/HTTPS/SSH/SSDP` | `AccessMode`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `HideCommunityStrings`, `HttpProtocolVersion`, `NTPServers`, `NetworkSuppliedServers`, `Port1`, `Port2`, `RMCPEnabled`, `RMCPPlusEnabled`, `iBMCBMC服务资源信息` |

### 4.1.2 查询当前根服务资源（差异 31）

- BMC section: `3.1.2`  method: `GET`
- PoDM URI: `/redfish/v1`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `ChassisOverview`, `Links/Sessions`, `Oem/Huawei`, `ResourceNodes` | `ComponentIntegrity`, `DeepOperations`, `DeepPATCH`, `DeepPOST`, `ExcerptQuery`, `ExpandAll`, `ExpandQuery`, `Fabrics`, `FilterQuery`, `FilterQueryComparisonOperations`, `FilterQueryCompoundOperations`, `JobService`, `LCNService`, `Levels`, `Links`, `MaxLevels`, `NoLinks`, `ObservabilityService`, `OnlyMemberQuery`, `Product`, `ProtocolFeaturesSupported`, `SelectQuery`, `StartupDurationSeconds`, `StartupState`, `TelemetryService`, `TopSkipQuery`, `Vendor` |

### 4.2.5 修改SNMP资源属性（差异 30）

- BMC section: `3.2.24`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SnmpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `If-Match` |
| body | — | `AlarmSeverity`, `BobEnabled`, `CommunityName`, `LongPasswordEnabled`, `PasswordPattern`, `PasswordRulePolicy`, `RWCommunityEnabled`, `ReadOnlyCommunity`, `ReadWriteCommunity`, `ServiceEnabled`, `SnmpTrapNotification`, `SnmpV1Enabled`, `SnmpV1V2CLoginRule`, `SnmpV2CEnabled`, `SnmpV3Enabled`, `TrapMode`, `TrapServerIdentity`, `TrapV3User`, `TrapVersion` |
| response | — | `@Redfish.ActionInfo`, `Actions`, `BobEnabled`, `Links`, `LoginRule`, `PasswordPattern`, `PasswordRulePolicy`, `SNMP资源信息`, `TrapMode`, `target` |

### 4.3.2 查询指定系统资源信息（差异 29）

- BMC section: `3.3.2`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `NpuBoardSerialNumber`, `Oem/Huawei/Public`, `Slot`, `TenantID`, `Type`, `Value`, `VncConfig` | `ActivatedSessionsType`, `AutoOSLockEnabled`, `AutoOSLockKey`, `AutoOSLockType`, `BSasCtrlSdkVersion`, `BWUWaveTitle`, `DelaySecondsAfterCpuThermalTrip`, `DisableKeyboardDuringBiosStartup`, `EnergySavingEnabled`, `HotSpare`, `KVMSettings`, `MaximumNumberOfSessions`, `NumberOfActiveSessions`, `PersistentUSBConnectionEnabled`, `PowerMode`, `PowerOnAfterCpuThermalTrip`, `SSDMediaLifeLeftPercentThreshold`, `SecureBoot`, `Spans`, `VirtualMedia`, `VncSettings`, `Volumes` |

### 4.10.2.8 修改SSL证书更新服务资源信息（差异 28）

- BMC section: `3.2.62`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/1/SecurityService/CertUpdateService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SecurityService/CertUpdateService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `manager_id` |
| header | `Content-Type`, `x-non-renewal-session` | — |
| body | — | `AlternativeNames`, `CMPConfig`, `CommonName`, `Country`, `Email`, `InternalName`, `Location`, `OrgName`, `OrgUnit`, `State` |
| response | `CAServerCMPPath` | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber`, `ServerCert`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo` |

### 4.10.2.4 修改会话策略（差异 27）

- BMC section: `3.5.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/SessionService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| body | `Oem/Huawei`, `Redfish.SessionMode`, `WebUI.SessionMode`, `WebUI.SessionTimeoutMinutes` | `HuaweiPublic`, `KVM`, `Oem`, `Redfish`, `SessionMode`, `SessionTimeoutMinutes`, `VNC`, `ValidateSsoClient`, `Video`, `WebSessionMode`, `WebSessionTimeoutMinutes`, `WebUI` |
| response | `Health`, `Huawei`, `Oem`, `ServiceEnabled`, `State`, `Status` | `SessionService资源信息`, `WebSessionMode`, `WebSessionTimeoutMinutes` |

### 4.10.1.1 创建用户（差异 27）

- BMC section: `3.5.9`  method: `POST`
- PoDM URI: `/redfish/v1/AccountService/Accounts`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `X-Auth-Token`, `x-non-renewal-session` | — |
| body | — | `ReauthKey` |
| response | `@odata.context`, `@odata.id`, `@odata.type`, `AccountInsecurePromptEnabled`, `Actions`, `Deleteable`, `Enabled`, `FirstLoginPolicy`, `Huawei`, `Links`, `Locked`, `LoginInterface`, `LoginRule`, `Name`, `Oem`, `Password`, `PasswordValidityDays`, `Role`, `RoleId`, `SNMPEncryptPwdInit`, `SnmpV3AuthProtocol`, `SnmpV3PrivPasswd`, `SnmpV3PrivProtocol`, `UserName` | — |

### 4.7.3 模拟测试事件（差异 25）

- BMC section: `3.9.3`  method: `POST`
- PoDM URI: `/redfish/v1/EventService/Actions/EventService.SubmitTestEvent`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@odata.context`, `@odata.id`, `Addinfo`, `Context`, `EventId`, `EventSubject`, `EventTimestamp`, `EventType`, `Events`, `Id`, `Level`, `Name`, `OriginOfCondition`, `ServerIdentity`, `ServerLocation`, `alarmStatus`, `locationInfo`, `neName`, `neType`, `neUID`, `objectName`, `objectType`, `objectUID`, `specificProblem`, `specificProblemID` |

### 4.2.19 查询PoDManager指定网卡信息（差异 25）

- BMC section: `3.2.42`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/EthernetInterfaces/{ethernetinterface_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `AdaptiveFlag`, `AdaptivePort`, `Chassis`, `ChassisLanSubNet`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link`, `Links`, `ManagementNetworkPort`, `ManagementNetworkPort@Redfish.AllowableValues`, `ManagementNetworkPortMembers`, `NetworkPortMode`, `OperatingMode`, `PortNumber`, `StaticNameServers`, `SwitchConnectionPortIDs`, `SwitchConnections`, `SwitchManagementIP`, `Type`, `UseNTPServers`, `VLAN` |

### 4.10.1.4 查询全量用户（差异 25）

- BMC section: `3.6.3`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/Accounts`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `Huawei`, `Oem`, `SnmpV3AuthPasswd`, `UserType` | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `KeyUsage`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `PublicKeyLengthBits`, `RevokedDate`, `RevokedState`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo`, `target` |

### 4.10.1.2 修改用户（差异 25）

- BMC section: `3.6.7`  method: `PATCH`
- PoDM URI: `/redfish/v1/AccountService/Accounts/{account_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| body | `CurrentPassword` | `HuaweiPublic`, `UserName` |
| response | `Huawei`, `Oem`, `Role` | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `RevokedDate`, `RevokedState`, `Roles`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `ValidFrom`, `ValidTo`, `target` |

### 4.2.16 查询PoDManager服务信息（差异 24）

- BMC section: `3.2.44`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/NetworkProtocol`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | — | `AccessMode`, `Certificates`, `Certificates.@odata.id`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `FQDN`, `HideCommunityStrings`, `HostName`, `HttpProtocolVersion`, `NTPServers`, `NetworkSuppliedServers`, `NotifyEnabled`, `NotifyIPv6Scope`, `NotifyMulticastIntervalSeconds`, `NotifyTTL`, `Port1`, `Port2`, `RMCPEnabled`, `RMCPPlusEnabled`, `iBMCBMC服务集合资源信息` |

### 4.7.9 修改事件订阅资源（差异 23）

- BMC section: `3.9.9`  method: `PATCH`
- PoDM URI: `/redfish/v1/EventService/Subscriptions/{id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `Context`, `HttpHeaders` | — |
| response | — | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `OriginResources`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |

### 4.5.1 查询升级服务资源信息（差异 22）

- BMC section: `3.7.1`  method: `GET`
- PoDM URI: `/redfish/v1/UpdateService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Members`, `Members@odata.count`, `Oem/Huawei/`, `Tasks` | `@Redfish.ActionInfo`, `AutoFirmwareActivationEnable`, `CertificateRevocationLists`, `Certificates`, `FirmwareIntegrity`, `FirmwareToTakeEffect`, `FirmwareType`, `InbandFirmwareUpdateEnabled`, `MaxImageSizeBytes`, `RelatedFirmwareItems`, `StagedTime`, `StagedVersion`, `SyncUpdateState`, `Task`, `UpdateService.ActivateBios`, `UpdateService.SimpleUpdate`, `UpdateService.StartActivate`, `UpdateService.StartSyncUpdate` |

### 4.3.51 查询指定处理器资源信息（差异 21）

- BMC section: `3.3.50`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Processors/{processor_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `BoardPartNumber`, `InfoRomVersion`, `Inventory`, `Oem/Huawei/Public`, `OperatingSpeedsMHz`, `SlotNumber` | `AggregateTotalCount`, `BandWidth`, `Bank`, `Boards`, `ErrorCount`, `Family`, `Metrics`, `NpuBoardSerialNumber`, `OtherParameters`, `PhysicalAddress`, `Ports`, `RowColumn`, `StackPcId`, `Time`, `TotalEnabledCores` |

### 4.7.8 查询事件订阅资源（差异 21）

- BMC section: `3.9.8`  method: `GET`
- PoDM URI: `/redfish/v1/EventService/Subscriptions/{id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `OriginResources`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |

### 4.4.28 修改指定驱动器属性（差异 20）

- BMC section: `3.4.37`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/Drives/{drives_id}`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `drive_id` | `drives_id` |
| body | — | `@odata.id`, `BootEnable`, `BootPriority`, `FirmwareStatus`, `HotspareType`, `HuaweiPublic`, `IndicatorLED`, `LocationIndicatorActive`, `Oem`, `PatrolState`, `SpareforLogicalDrives` |
| response | `Oem/Huawei` | `Assembly`, `DriveFormFactor`, `LocationIndicatorActive`, `Metrics`, `PartNumber`, `PhysicalLocation` |

### 4.3.13 设置虚拟媒体资源（差异 19）

- BMC section: `3.3.80`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia/CD`
- BMC URI: `/redfish/v1/Systems/system_id /VirtualMedia/CD`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | — |
| header | `Content-Type`, `If-Match` | — |
| body | `EncryptionEnabled`, `FloppyDriveEnabled` | `EjectPolicy`, `EjectTimeout`, `Password`, `UserName` |
| response | `EncryptionConfigurable`, `EncryptionEnabled`, `FloppyDriveEnabled`, `Oem/Huawei`, `TransferMethod`, `TransferProtocolType`, `WriteProtected` | `EjectPolicy`, `EjectTimeout`, `Password` |

### 4.2.4 查看SNMP资源信息（差异 19）

- BMC section: `3.2.23`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SnmpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@Redfish.ActionInfo`, `Actions`, `BobEnabled`, `Links`, `LoginRule`, `LongPasswordEnabled`, `PasswordPattern`, `PasswordRulePolicy`, `RWCommunityEnabled`, `ReadOnlyCommunity`, `ReadWriteCommunity`, `SNMP资源信息`, `SnmpV1Enabled`, `SnmpV2CEnabled`, `SnmpV3Enabled`, `SystemContact`, `SystemLocation`, `TrapMode`, `target` |

### 4.2.110 修改FDMService服务资源属性（差异 18）

- BMC section: `3.2.125`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/FDMService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| body | `MemPoorContactAlarmEnabled` | `CPUFaultIsolationSubFunction`, `CacheWayFPCEnabled`, `CoreIsolationAlarmThreshold`, `FPCSubFunctionSwitch`, `MemFaultIsolationSubFunctionSwitch`, `MemRowSparingEnabled`, `MemoryDynamicRemappingEnabled`, `MemoryOnChip`, `NpuHbmFPCSubFunctionSwitch` |
| response | — | `CPUFaultIsolationSubFunction`, `CacheWayFPCEnabled`, `CoreIsolationAlarmThreshold`, `FDMService资源的信息`, `MemRowSparingEnabled`, `MemoryDynamicRemappingEnabled` |

### 4.10.1.5 查询指定用户（差异 18）

- BMC section: `3.6.4`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/Accounts/{member_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | — |
| response | `Huawei`, `LastLoginIP`, `Oem` | `@Redfish.ActionInfo`, `FingerPrint`, `HostBootstrapAccount`, `IssueBy`, `IssueTo`, `LastLoginIp`, `RevokedDate`, `RevokedState`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `ValidFrom`, `ValidTo`, `target` |

### 4.10.2.7 查询SSL证书更新服务资源信息（差异 17）

- BMC section: `3.2.61`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/1/SecurityService/CertUpdateService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SecurityService/ CertUpdateService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `manager_id` |
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | — | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber`, `ServerCert`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo` |

### 4.2.89 添加工作记录（差异 16）

- BMC section: `3.2.111`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/WorkRecord/Actions/WorkRecord.AddRecord`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `@odata.context`, `@odata.id`, `@odata.type`, `Actions`, `Address`, `Details`, `Id`, `Name`, `NextAvailableId`, `Records`, `Time`, `User`, `WorkRecord.AddRecord`, `WorkRecord.DeleteRecord`, `WorkRecord.ModifyRecord` | — |

### 4.2.90 删除工作记录（差异 16）

- BMC section: `3.2.112`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/WorkRecord/Actions/WorkRecord.DeleteRecord`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `@odata.context`, `@odata.id`, `@odata.type`, `Actions`, `Address`, `Details`, `Id`, `Name`, `NextAvailableId`, `Records`, `Time`, `User`, `WorkRecord.AddRecord`, `WorkRecord.DeleteRecord`, `WorkRecord.ModifyRecord` | — |

### 4.2.91 修改工作记录（差异 16）

- BMC section: `3.2.113`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/WorkRecord/Actions/WorkRecord.ModifyRecord`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `@odata.context`, `@odata.id`, `@odata.type`, `Actions`, `Address`, `Details`, `Id`, `Name`, `NextAvailableId`, `Records`, `Time`, `User`, `WorkRecord.AddRecord`, `WorkRecord.DeleteRecord`, `WorkRecord.ModifyRecord` | — |

### 4.2.39 创建SP服务的OS安装配置（差异 15）

- BMC section: `3.2.77`  method: PoDM `GET` / BMC `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPOSInstallPara`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `BootEffective`, `BootParameters`, `Position`, `VGName`, `device` | `Device`, `IPv4RouteSettings`, `IPv6RouteSettings`, `NetCfg`, `Packages` |
| response | — | `FirstBootScriptFile`, `IPv4RouteSettings`, `IPv6RouteSettings`, `Metric`, `TableId` |

### 4.10.7.1 导入CA证书（差异 15）

- BMC section: `3.12.4`  method: `POST`
- PoDM URI: `/redfish/v1/CertificateService/Actions/CertificateService.ImportCACertificate`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| body | `Text` | `Type` |
| response | — | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState`, `TaskStatus` |

### 4.2.10 修改NTP资源（差异 15）

- BMC section: `3.2.21`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/NtpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `ifmatch_value` | `If-Match` |
| body | — | `AlternateNtpServer`, `ExtraNtpServer`, `MaxPollingInterval`, `MinPollingInterval`, `NtpAddressOrigin`, `PreferredNtpServer`, `ServerAuthenticationEnabled`, `ServiceEnabled` |
| response | — | `Actions`, `Id`, `NTPKeyStatus`, `NTP资源信息`, `Name` |

### 4.10.7.5 导入CA证书吊销列表（差异 15）

- BMC section: `3.12.6`  method: `POST`
- PoDM URI: `/redfish/v1/CertificateService/Actions/CertificateService.ImportCACertificateCRL`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `X-Auth-Token`, `x-non-renewal-session` | — |
| body | `Id` | `CertId` |
| response | — | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState`, `TaskStatus` |

### 4.1.3 修改当前根服务资源（差异 14）

- BMC section: `3.1.3`  method: `PATCH`
- PoDM URI: `/redfish/v1`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| response | `AssetService`, `ChassisOverview`, `Links/Sessions`, `MajorVersion`, `Oem/Huawei`, `ResourceNodes` | `Fabrics`, `JobService`, `KerberosEnabled`, `ObservabilityService`, `Product`, `Vendor` |

### 4.2.50 创建SP服务的诊断配置（差异 14）

- BMC section: `3.2.88`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPDiagnose`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `Managers` | `manager_id` |
| body | — | `ActionOnCompleted`, `AssetVerification`, `DeviceType`, `Diagnose`, `ItemMode`, `Mode`, `RebootDelayMinutes`, `SubItems` |
| response | — | `AssetVerification`, `CountItem`, `CountValue`, `CountVerification` |

### 4.6.3 查询指定任务资源信息（差异 14）

- BMC section: `3.8.4`  method: `GET`
- PoDM URI: `/redfish/v1/TaskService/Tasks/{taskid}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Description`, `EndTime`, `EstimatedDuration`, `Message`, `MessageArgs`, `MessageId`, `MessageSeverity`, `Messages`, `PercentComplete`, `RelatedProperties`, `Resolution`, `Severity`, `SubTasks` |

### 4.10.4.2 创建会话（登录）（差异 14）

- BMC section: `3.5.3`  method: `POST`
- PoDM URI: `/redfish/v1/SessionService/Sessions`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `From`, `Ip`, `Mac`, `x-non-renewal-session` | — |
| body | — | `HuaweiPublic`, `Oem` |
| response | `FirstLoginPolicy`, `Oem`, `token` | `ClientOriginIPAddress`, `CreatedTime`, `OemSessionType`, `Roles`, `SessionType` |

### 4.2.75 查询全量告警信息（差异 13）

- BMC section: `3.2.153`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LogServices/EventLog`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Created`, `EntryType`, `EventId`, `EventSubject`, `EventType`, `HandlingSuggestion`, `Level`, `Message`, `MessageArgs`, `MessageId`, `Severity`, `SystemId` |

### 4.4.53 设置风扇组、泵组转速批量下发（差异 13）

- BMC section: `3.4.68`  method: PoDM `GET` / BMC `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/Actions/Oem/{{OemIdentifier}}/ThermalControlUnitGroup.SetExpectedSpeedPercent`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `fan_id` | — |
| header | `Content-Type` | — |
| body | — | `Oem`, `ThermalControlUnitGroup` |
| response | `@odata.type`, `Message`, `MessageArgs`, `MessageId`, `RelatedProperties`, `Resolution`, `Severity`, `code`, `message` | — |

### 4.6.6 查询指定子任务资源信息（差异 13）

- BMC section: `3.8.7`  method: `GET`
- PoDM URI: `/redfish/v1/TaskService/Tasks/{taskid}/SubTasks/{subtaskid}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `subtaskid`, `taskid` | — |
| response | `Oem/Huawei` | `Description`, `EndTime`, `EstimatedDuration`, `MessageArgs`, `MessageId`, `MessageSeverity`, `RelatedProperties`, `Resolution`, `Severity`, `StartTime` |

### 4.3.16 查询虚拟SP U盘资源（差异 12）

- BMC section: `3.2.16`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia/USBStick`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VirtualMedia/USBStick`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| response | `Message`, `Oem/Huawei`, `StartTime`, `TaskPercentage`, `TaskState` | `ConnectedVia`, `Image`, `ImageName`, `Inserted`, `MediaTypes` |

### 4.3.33 修改指定控制器资源信息（差异 12）

- BMC section: `3.3.24`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `ConfiguredDrive`, `HuaweiPublic`, `MaintainPDFailHistory`, `Oem`, `StorageControllers`, `UnconfiguredDrive`, `VolumeConsistencyCheckConfig`, `WriteCachePolicy` |
| response | `Oem/Huawei/Public`, `PHYId`, `SerialNumber` | `PhyId` |

### 4.3.49 修改BIOS策略重配设置资源属性（差异 12）

- BMC section: `3.3.41`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios/PolicyConfig/Settings`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `If-Match` | — |
| body | — | `CETh`, `Demt`, `Funnel`, `PSEn`, `PdEn`, `PdPrd`, `PsFunnel`, `RefreshRate`, `UnitTime` |
| response | — | `BIOS策略重配设置资源信息` |

### 4.4.20 查询网络适配器单个资源信息（差异 12）

- BMC section: `3.4.19`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{networkadapters_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Actions`, `Assembly`, `Metrics`, `NetworkDeviceFunctions`, `Ports`, `PreloadPortCount`, `PreloadPortCountAllowableValues`, `Processors`, `RootBDFs`, `SerialNumber`, `target` |

### 4.4.25 查询网络端口上接的光模块资源信息（差异 12）

- BMC section: `3.4.31`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Transceivers/{transceivers_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@Redfish.ActionInfo`, `Actions`, `ContaminationDetection`, `LaneMappings`, `Location`, `LocationOrdinalValue`, `LocationType`, `PartLocation`, `PartLocationContext`, `RXFCSErrors`, `ServiceLabel`, `target` |

### 4.10.9.5 修改具体域控制器的信息（差异 12）

- BMC section: `3.6.25`  method: `PATCH`
- PoDM URI: `/redfish/v1/AccountService/LdapService/LdapControllers/{member_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| body | `CertificateVerificationEnabled`, `MemberId` | `BindDN`, `BindPassword`, `GroupDomain`, `LdapGroups`, `LdapPort`, `LdapServerAddress`, `UserDomain` |
| response | — | `GroupDomain` |

### 4.8.5 查询数据表资源信息（差异 12）

- BMC section: `3.11.8`  method: `GET`
- PoDM URI: `/redfish/v1/DataAcquisitionService/DataAcquisitionReport`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `component`, `end_time`, `metric`, `serial_number`, `start_time` | — |
| query | — | `ComponentType`, `EndTime`, `MetricType`, `SerialNumber`, `StartTime` |
| response | `MetricInfo` | `IndicatorLED` |

### 4.9.13 创建触发器（差异 12）

- BMC section: `3.15.13`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/Triggers`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `@odata.id`, `Description`, `Id`, `Links`, `LowerCritical`, `LowerWarning`, `MetricIds`, `MetricReportDefinitions`, `Name`, `NumericThresholds`, `UpperCritical`, `UpperWarning` |

### 4.2.63 查询诊断服务资源（差异 11）

- BMC section: `3.2.100`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `DeteriorationPredictionEnabled`, `DiagnosticService.ExportDiagnosticMetrics`, `DiagnosticService.StartCollectDrivesLog`, `DiskSubhealthFunction`, `DrivesLogCollectEnable`, `DrivesLogCollectInterval`, `LifespanEstimateAlarmEnabled`, `LifespanEstimateEnabled`, `OpticalModuleSubhealthFunction`, `PRBSTest` |

### 4.2.13 修改LLDP服务资源信息（差异 11）

- BMC section: `3.2.130`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LldpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| body | — | `TxDelaySeconds`, `TxHold`, `TxIntervalSeconds`, `WorkMode` |
| response | — | `LLDP服务资源信息`, `TxDelaySeconds`, `TxHold`, `TxIntervalSeconds`, `WorkMode` |

### 4.3.19 配置以太网（差异 11）

- BMC section: `3.3.8`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/EthernetInterfaces/{ethernetinterface_id}/Actions/Oem/Huawei/Public/EthernetInterface.Configure`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `IPv4Addresses`, `IsOnBoo`, `LinkStatus` | — |
| body | — | `IPv4Addresses`, `IsOnBoot`, `LinkStatus` |
| response | `Oem/Huawei/Public` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.4.10 修改指定电源属性（差异 11）

- BMC section: `3.4.11`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Power`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `@odata.id`, `HuaweiPublic`, `Mode`, `Oem`, `PowerControl`, `PowerLimit`, `PowerMetricsExtended`, `PresetLimitInWatts`, `Redundancy`, `RedundancySet` |
| response | `Oem/Huawei` | — |

### 4.4.50 查询漏液检测（差异 11）

- BMC section: `3.4.65`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/LeakDetection/LeakDetectors/{LeakDetector_id}`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/LeakDetectors/LeakDetector_id`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `LeakDetector_id` | — |
| response | — | `LeakDetectorType`, `Location`, `Manufacturer`, `Model`, `PartLocation`, `PartNumber`, `PhysicalContext`, `Reference`, `SerialNumber`, `ServiceLabel` |

### 4.7.2 修改事件服务资源（差异 11）

- BMC section: `3.9.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/EventService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `DeliveryRetryAttempts`, `DeliveryRetryIntervalSeconds`, `HuaweiPublic`, `Oem`, `SnmpReportType` |
| response | `Oem/Huawei` | `DeliveryRetryAttempts`, `DeliveryRetryIntervalSeconds`, `EventService资源信息`, `SnmpReportType`, `Status` |

### 4.2.28 查询Syslog资源信息（差异 10）

- BMC section: `3.2.31`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SyslogService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `ReportType`, `RootCertificate.Issuer`, `RootCertificate.KeyUsage`, `RootCertificate.PublicKeyLengthBits`, `RootCertificate.SerialNumber`, `RootCertificate.SignatureAlgorithm`, `RootCertificate.Subject`, `RootCertificate.ValidNotAfter`, `RootCertificate.ValidNotBefore`, `Syslog资源信息` |

### 4.10.8.2 更新系统主密钥（差异 10）

- BMC section: `3.2.52`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/1/SecurityService/Actions/SecurityService.UpdateMasterKey`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SecurityService/Actions/SecurityService.UpdateMasterKey`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `manager_id` |
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `@odata.content`, `Huawei`, `Oem` | `@odata.context`, `Description`, `PercentComplete`, `TaskStatus` |

### 4.3.7 修改VNC资源属性（差异 10）

- BMC section: `3.2.69`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VncService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VNCService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| header | `Content-Type`, `If-Match` | — |
| body | — | `LoginRule`, `PasswordPattern`, `PasswordRulePolicy` |
| response | — | `DisableKeyboardDuringBiosStartup`, `PasswordPattern`, `PasswordRulePolicy` |

### 4.2.51 查询SP服务的诊断配置资源（差异 10）

- BMC section: `3.2.89`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPDiagnose/1`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `ActionOnCompleted`, `AssetVerification`, `CountItem`, `CountValue`, `CountVerification`, `DumpEnabled`, `LogDump`, `PushTimeoutMinutes`, `RebootDelayMinutes`, `SP服务的诊断配置资源的信息` |

### 4.4.27 查询指定驱动器资源信息（差异 10）

- BMC section: `3.4.36`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/{drives}/{drive_id}`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `drives` |
| response | `Oem/Huawei` | `Assembly`, `DriveFormFactor`, `FormFactor`, `LocationIndicatorActive`, `Metrics`, `PartNumber`, `PhysicalLocation`, `SlotPowerState` |

### 4.4.35 查询指定PCIe设备资源信息（差异 10）

- BMC section: `3.4.47`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `DeviceType`, `HotPluggable`, `Lanes`, `MaxPCIeType`, `PCIeType`, `PowerState`, `Processors`, `ReadyToRemove`, `SlotType` |

### 4.2.3 修改管理资源信息（差异 10）

- BMC section: `3.2.3`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `Content-Type`, `If-Match` |
| body | — | `GraphicalConsole`, `HuaweiPublic`, `LoginRule`, `Oem`, `Stateless`, `SystemManagerInfo` |
| response | `Manager.SetFusionPartition`, `Oem/Huawei` | — |

### 4.4.9 查询指定机柜电源信息（差异 10）

- BMC section: `3.4.10`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Power`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `BatteryMetricsExtended`, `BatteryPresenceState`, `EODAlarmState`, `PSUInputAStatus`, `PSUInputBStatus`, `RatedCapacityWattHour`, `RemainCapacityWattHour`, `VinChannelAVoltage`, `VinChannelBVoltage` |

### 4.4.14 查询指定机柜电源子系统信息（差异 10）

- BMC section: `3.4.15`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Allocation`, `CapacityWatts`, `MaxSupportedInGroup`, `MinNeededInGroup`, `PowerSupplies`, `PowerSupplyRedundancy`, `RedundancyGroup`, `RedundancyType`, `Status` |

### 4.10.4.3 查询指定会话（差异 10）

- BMC section: `3.5.5`  method: `GET`
- PoDM URI: `/redfish/v1/SessionService/Sessions/{session_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `huawei`, `oem` | `AccountInsecurePromptEnabled`, `ClientOriginIPAddress`, `CreatedTime`, `OemSessionType`, `Roles`, `SessionType` |

### 4.3.14 连接虚拟媒体（差异 9）

- BMC section: `3.2.14`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Oem/Huawei/Actions/VirtualMedia.VmmControl`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD/Oem/Huawei/Public/Actions/VirtualMedia.VmmControl`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| body | — | `Password`, `TransferProtocolType`, `UserName` |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.3.18 查询指定主机以太网接口资源信息（差异 9）

- BMC section: `3.3.7`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/EthernetInterfaces/{ethernetinterface_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | `EthernetInterfaceType`, `Links`, `MTUSize`, `Ports`, `VLAN`, `VLANEnable`, `VLANId`, `VLANPriority` |

### 4.4.46 修改指定机柜泵资源信息（差异 9）

- BMC section: `3.4.61`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `If-Match` | — |
| body | — | `FanSpeedDeviationThresholdPercent`, `HuaweiPublic`, `LiquidCoolingUnitsLevel`, `LiquidManualModeTimeoutSeconds`, `LiquidSpeedAdjustmentMode`, `Oem` |
| response | — | `FanSpeedDeviationThresholdPercent` |

### 4.5.4 批量升级固件（差异 9）

- BMC section: `3.7.8`  method: `POST`
- PoDM URI: `/redfish/v1/UpdateService/Actions/Oem/Huawei/UpdateService.ParallelUpdate`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| body | `ImageURI`, `SignatureURI`, `Targets`, `TransferProtocol` | `Packages`, `Stage` |
| response | `Oem/Huawei` | `Description` |

### 4.6.4 查询指定任务运行信息（差异 9）

- BMC section: `3.8.5`  method: `GET`
- PoDM URI: `/redfish/v1/TaskService/Tasks/{taskid}/Monitor`
- BMC URI: `/redfish/v1/TaskService/Tasks/{task_id}/Monitor`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `taskid` | `task_id` |
| response | — | `@odata.type`, `Message`, `MessageArgs`, `MessageId`, `RelatedProperties`, `Resolution`, `Severity` |

### 4.2.109 查询FDMService服务资源（差异 8）

- BMC section: `3.2.124`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/FDMService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `CPUFaultIsolationSubFunction`, `CacheWayFPCEnabled`, `CoreIsolationAlarmThreshold`, `CpuFPC`, `FDMService资源的信息`, `MemRowSparingEnabled`, `MemoryDynamicRemappingEnabled`, `NpuFPC` |

### 4.4.23 修改网络端口单个资源信息（差异 8）

- BMC section: `3.4.29`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{networkadapters_id}/NetworkPorts/{networkports_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `If-Match` | — |
| body | — | `HuaweiPublic`, `LldpService`, `Oem` |
| response | `LldpService`, `Oem/Huawei` | `LldpEnabled` |

### 4.4.36 修改指定PCIe设备资源信息（差异 8）

- BMC section: `3.4.48`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `HuaweiPublic`, `Oem`, `ReadyToRemove`, `UEFILogLevel` |
| response | `Oem/Huawei`, `PCIeCardType`, `VrdFirmwareVersion` | `ReadyToRemove` |

### 4.4.48 查询漏液检测系统信息（差异 8）

- BMC section: `3.4.63`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/LeakDetection`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `@odata.context`, `@odata.type`, `Id`, `Name` | `Health`, `HealthRollup`, `State`, `Status` |

### 4.9.15 修改指定触发器资源信息（差异 8）

- BMC section: `3.15.15`  method: PoDM `GET` / BMC `PATCH`
- PoDM URI: `/redfish/v1/TelemetryService/Triggers/{id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `MetricType` | `@odata.id`, `Links`, `LowerCritical`, `LowerWarning`, `NumericThresholds`, `UpperCritical`, `UpperWarning` |

### 4.4.45 查询指定机柜泵资源信息（差异 8）

- BMC section: `3.4.60`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `CoolantConnectorRedundancy`, `FanRedundancy`, `FanSpeedDeviationThresholdPercent`, `MaxSupportedInGroup`, `MinNeededInGroup`, `RedundancyGroup`, `RedundancyType`, `ThermalMetrics` |

### 4.10.2.6 修改证书策略（差异 8）

- BMC section: `3.12.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/CertificateService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| body | — | `CRLEnabled`, `HuaweiPublic`, `Oem` |
| response | `Oem/Huawei` | `CRLEnabled`, `CertificateService资源信息` |

### 4.2.2 查询指定管理资源信息（差异 7）

- BMC section: `3.2.2`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Manager.QuickDump`, `Manager.ResetToDefaults`, `Scope`, `ShelfPowerButtonMode`, `VenderName`, `WirelessService` |

### 4.2.25 导出日志信息（差异 7）

- BMC section: `3.2.116`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Actions/Oem/Huawei/LogService.ExportLog`
- BMC URI: `/redfish/v1/Managers/{manager_id}/LogServices/{logservice_id}/Actions/Oem/Huawei/Public/LogService.ExportLog`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `logservices_id` | `logservice_id` |
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.97 下发PRBS测试配置（差异 7）

- BMC section: `3.2.159`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest/Actions/PRBSTest.Config`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| body | `TestObjects` | `ConfigType`, `DurationSeconds`, `PatternId`, `TestObjectId` |
| response | `Oem/Huawei` | — |

### 4.3.40 创建逻辑盘（差异 7）

- BMC section: `3.3.32`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Volumes`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `AssociatedVolumes`, `HuaweiPublic`, `Oem` |
| response | `Oem/Huawei/Public` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.4.39 指定PCIe设备资源导入https证书（差异 7）

- BMC section: `3.4.51`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}/Actions/Oem/Huawei/PCIeDevices.ImportHttpsCert`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/pciedevices_id /Actions/Oem/Huawei/Public/PCIeDevices.ImportHttpsCert`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `account_id`, `pciedevices_id` | — |
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.4.40 查询指定PCIe功能资源信息（差异 7）

- BMC section: `3.4.53`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}/Functions/{functions_id}`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}/PCIeFunctions/functions_id（推荐使用）`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `functions_id` | — |
| response | `EthernetInterfaces/Drives/StorageControllers`, `Oem/Huawei` | `ClassCode`, `FunctionProtocol`, `FunctionType`, `SegmentNumber` |

### 4.9.1 查询遥测服务资源信息（差异 7）

- BMC section: `3.15.1`  method: `GET`
- PoDM URI: `/redfish/v1/TelemetryService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `MetricDefinitions`, `MetricReportDefinitions`, `MetricReports`, `Triggers` | `TelemetryService.ResetMetricReportDefinitionsToDefaults`, `TelemetryService.ResetTriggersToDefaults`, `TelemetryService.SubmitTestMetricReport` |

### 4.9.2 修改遥测服务资源信息（差异 7）

- BMC section: `3.15.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/TelemetryService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `MetricDefinitions`, `MetricReportDefinitions`, `MetricReports`, `Triggers` | `TelemetryService.ResetMetricReportDefinitionsToDefaults`, `TelemetryService.ResetTriggersToDefaults`, `TelemetryService.SubmitTestMetricReport` |

### 4.2.9 查询NTP资源（差异 7）

- BMC section: `3.2.20`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/NtpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `NtpKeyUploaded` | `Actions`, `CurrentPollingIntervalSeconds`, `Id`, `NTPKeyStatus`, `NTP配置资源信息`, `Name` |

### 4.10.2.3 查询会话策略（差异 7）

- BMC section: `3.5.1`  method: `GET`
- PoDM URI: `/redfish/v1/SessionService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `Huawei`, `Oem` | `SessionService资源信息`, `WebSessionMode`, `WebSessionTimeoutMinutes` |

### 4.3.15 断开虚拟媒体（差异 6）

- BMC section: `3.2.15`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia/CD/Oem/Huawei/Actions/VirtualMedia.VmmControl`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD/Oem/Huawei/Public/Actions/VirtualMedia.VmmControl`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.40 查询SP服务的OS安装配置资源（差异 6）

- BMC section: `3.2.78`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPOSInstallPara/{osid}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `FirstBootScriptFile`, `IPv4RouteSettings`, `IPv6RouteSettings`, `Metric`, `OS安装配置资源信息`, `TableId` |

### 4.3.26 查询指定内存资源信息（差异 6）

- BMC section: `3.3.15`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Memory/{memory_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | `BomNumber`, `ControllerTemperatureCelsius`, `EccCount`, `MediumTemperatureCelsius`, `RemainingServiceLifePercent` |

### 4.3.60 批量查询处理器资源信息（差异 6）

- BMC section: `3.3.70`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/ProcessorView`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `ECCInfo`, `OperatingSpeedsMHz` | `EccInfo`, `MultiBitIsolatedPages`, `OperatingSpeedMHz`, `SingleBitIsolatedPages` |

### 4.4.52 查询风扇单个资源信息（差异 6）

- BMC section: `3.4.67`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/Fans/{fan_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `DataSourceUri`, `Location`, `LocationOrdinalValue`, `LocationType`, `PartLocation`, `ServiceLabel` |

### 4.10.1.3 删除用户（差异 6）

- BMC section: `3.6.6`  method: `DELETE`
- PoDM URI: `/redfish/v1/AccountService/Accounts/{account_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `@Message.ExtendedInfo`, `Code`, `Error` | `code` |

### 4.5.5 生效固件（差异 6）

- BMC section: `3.7.7`  method: `POST`
- PoDM URI: `/redfish/v1/UpdateService/Actions/Oem/Huawei/UpdateService.StartActivate`
- BMC URI: `/redfish/v1/UpdateService/Actions/Oem/Huawei/Public/UpdateService.StartActivate`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| body | `Targets` | — |
| response | — | `Description`, `Messages`, `PercentComplete`, `TaskStatus` |

### 4.7.1 查询事件服务资源（差异 6）

- BMC section: `3.9.1`  method: `GET`
- PoDM URI: `/redfish/v1/EventService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `DeliveryRetryAttempts`, `DeliveryRetryIntervalSeconds`, `EventService资源信息`, `SnmpReportType`, `Status` |

### 4.8.1 查询数据采集服务资源（差异 6）

- BMC section: `3.11.1`  method: `GET`
- PoDM URI: `/redfish/v1/DataAcquisitionService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `DataAcquisitionReport` | `DataAcquisitionService资源信息`, `DataSource@Redfish.AllowableValues`, `HwDataAcquisitionService.ClearHistoryData`, `HwDataAcquisitionService.DataFiltering`, `HwDataAcquisitionService.ExportAcquisitionData` |

### 4.10.2.5 查询证书策略（差异 6）

- BMC section: `3.12.1`  method: `GET`
- PoDM URI: `/redfish/v1/CertificateService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `CACertificates`, `Oem/Huawei` | `CRLEnabled`, `CertificateService资源信息` |

### 4.2.86 更新SP相关的schema文件（差异 5）

- BMC section: `3.2.74`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Actions/SPService.UpdateSchemaFiles`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.59 安装SP插件（差异 5）

- BMC section: `3.2.98`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Plugins`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| body | — | `PluginURIs` |
| response | — | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.69 导出录像（差异 5）

- BMC section: `3.2.103`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.ExportVideo`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.72 导出黑匣子（差异 5）

- BMC section: `3.2.106`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.ExportBlackBox`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.73 导出串口数据（差异 5）

- BMC section: `3.2.107`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.ExportSerialPortData`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.94 内存隔离联动模式下发隔离任务（差异 5）

- BMC section: `3.2.138`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/FPCService/Memory/Actions/Memory.ExecuteIsolation`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `SequenceNums` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.3.22 配置Bond（差异 5）

- BMC section: `3.3.11`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/NetworkBondings/{bond_id}/Actions/NetworkBonding.Configure`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei/Public` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.3.32 查询指定存储资源信息（差异 5）

- BMC section: `3.3.21`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public`, `PHYId` | `EpdSupported`, `JbodStateSupported`, `PhyId` |

### 4.3.39 删除指定逻辑盘（差异 5）

- BMC section: `3.3.31`  method: `DELETE`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Volumes/{volume_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei/Public` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.8.2 修改数据采集服务开关状态（差异 5）

- BMC section: `3.11.2`  method: `PATCH`
- PoDM URI: `/redfish/v1/DataAcquisitionService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `DataAcquisitionReport` | `DataSource@Redfish.AllowableValues`, `HwDataAcquisitionService.ClearHistoryData`, `HwDataAcquisitionService.DataFiltering`, `HwDataAcquisitionService.ExportAcquisitionData` |

### 4.8.3 清空“数据采集点信息表”（差异 5）

- BMC section: `3.11.6`  method: `POST`
- PoDM URI: `/redfish/v1/DataAcquisitionService/Actions/HwDataAcquisitionService.ClearHistoryData`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Huawei`, `Oem` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.11 导入NTP密钥（差异 5）

- BMC section: `3.2.22`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/NtpService/Actions/NtpService.ImportNtpKey`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `manager_id` |
| header | `Content-Type` | — |
| body | `type` | `Type` |
| response | — | `NTP服务器密钥导入信息` |

### 4.2.29 修改Syslog资源信息（差异 5）

- BMC section: `3.2.32`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SyslogService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `ifmatch_value` | `If-Match` |
| body | — | `ReportType`, `SyslogServers` |
| response | — | `ReportType` |

### 4.2.70 截图（差异 5）

- BMC section: `3.2.104`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.CaptureScreenShot`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.1.8 查询所有归档资源（差异 4）

- BMC section: `3.1.8`  method: `GET`
- PoDM URI: `/redfish/v1/Registries`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Base.v1_0_0`, `BiosAttributeRegistry.v1_0_1`, `iBMC.v1_0_0`, `iBMCEvents.v2_0_10` |

### 4.1.9 查询单个归档资源（差异 4）

- BMC section: `3.1.9`  method: `GET`
- PoDM URI: `/redfish/v1/Registries/{registries_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Base.v1_0_0`, `BiosAttributeRegistry.v1_0_1`, `PoDManager.v1_0_0`, `PoDManagerEvents.v2_0_10` | — |

### 4.3.9 修改KVM资源属性（差异 4）

- BMC section: `3.2.39`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/KvmService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/KvmService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| body | — | `DisableKeyboardDuringBiosStartup` |
| response | — | `DisableKeyboardDuringBiosStartup` |

### 4.3.10 设置KVM Key（差异 4）

- BMC section: `3.2.40`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/KvmService/Actions/KvmService.SetKvmKey`
- BMC URI: `/redfish/v1/Managers/{manager_id}/KvmService/Actions/KvmService.SetKvmKey`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| header | `Content-Type`, `If-Match` | — |

### 4.2.87 收集SP相关的日志信息（差异 4）

- BMC section: `3.2.75`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Actions/SPService.Dump`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | — | `Description`, `PercentComplete`, `TaskStatus` |

### 4.2.43 升级SP或者升级固件（差异 4）

- BMC section: `3.2.81`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPFWUpdate/{updateid}/Actions/SPFWUpdate.SimpleUpdate`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SPService/SPFWUpdate/{update_id}/Actions/SPFWUpdate.SimpleUpdate`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `updateid` | `update_id` |
| body | — | `ImageURI`, `SignalURI` |

### 4.2.26 查询日志集合资源信息（差异 4）

- BMC section: `3.2.117`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Entries`
- BMC URI: `/redfish/v1/Managers/{manager_id}/LogServices/{logservice_id}/Entries`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `logservices_id` | `logservice_id` |
| response | `Members@odata.nextLin` | `Members@odata.nextLink` |

### 4.3.30 配置VLAN（差异 4）

- BMC section: `3.3.19`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/EthernetInterfaces/{ethernetinterface_id}/VLANs/{vlan_id}/Actions/Oem/Huawei/Public/VLanNetworkInterface.Configure`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.4.59 修改电子保单信息（差异 4）

- BMC section: `3.3.73`  method: `PATCH`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/DigitalWarranty`
- BMC URI: `/redfish/v1/Systems/{system_id}/DigitalWarranty`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `chassis_id` | `system_id` |
| header | `Content-Type`, `If-Match` | — |

### 4.4.13 收集功率统计数据（差异 4）

- BMC section: `3.4.14`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Actions/Power.CollectHistoryData`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Actions/Power.CollectHistoryData`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `Description`, `PercentComplete`, `TaskStatus` |

### 4.4.49 查询漏液检测器集合（差异 4）

- BMC section: `3.4.64`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/ThermalSubsystem/LeakDetection/LeakDetectors`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/LeakDetectors`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Id`, `LeakDetectors` | `Members`, `Members@odata.count` |

### 4.10.7.2 删除CA证书（差异 4）

- BMC section: `3.12.5`  method: `POST`
- PoDM URI: `/redfish/v1/CertificateService/Actions/CertificateService.DeleteCACertificate`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| body | — | `Id` |
| response | — | `CA证书删除信息` |

### 4.3.12 查询虚拟媒体资源（差异 3）

- BMC section: `3.2.13`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia/CD`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VirtualMedia/CD`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| response | `Oem/Huawei` | — |

### 4.3.8 查询KVM资源（差异 3）

- BMC section: `3.2.38`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/KvmService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/KvmService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |
| response | — | `DisableKeyboardDuringBiosStartup` |

### 4.2.56 创建SP系统擦除配置（差异 3）

- BMC section: `3.2.94`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SystemErase`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| body | — | `Components` |
| response | — | `SP系统擦除配置的信息` |

### 4.2.27 查询日志资源信息（差异 3）

- BMC section: `3.2.118`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LogServices/{logservices_id}/Entries/{Entries_id}`
- BMC URI: `/redfish/v1/Managers/{manager_id}/LogServices/LogService_id/Entries/Entries_id`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `entries_id`, `logservices_id` | — |
| response | `Oem/Huawei` | — |

### 4.2.112 修改USB管理服务资源信息（差异 3）

- BMC section: `3.2.135`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/USBMgmtService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| response | — | `USB管理服务配置资源信息` |

### 4.2.113 查询场景化智能节能信息（差异 3）

- BMC section: `3.2.139`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/EnergySavingService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `EnergySavingStatus`, `EnergySavingStatusPerDomain`, `NPUSubsystem` |

### 4.2.116 设置TPCM服务信息（差异 3）

- BMC section: `3.2.149`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SecurityService/TpcmService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `ifmatch_value` | — |
| response | — | `Tpcm服务配置资源信息` |

### 4.10.7.3 查询CA证书集合资源信息（差异 3）

- BMC section: `3.2.150`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/1/Certificates`
- BMC URI: `/redfish/v1/Managers/{manager_id}/Certificates`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `manager_id` |
| header | `Content-Type`, `x-non-renewal-session` | — |

### 4.3.37 修改指定逻辑盘资源属性（差异 3）

- BMC section: `3.3.29`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Volumes/{volume_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `HuaweiPublic`, `Oem` |
| response | `Oem/Huawei/Public` | — |

### 4.3.52 修改指定CPU资源属性（差异 3）

- BMC section: `3.3.51`  method: `PATCH`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Processors/{cpu_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `HuaweiPublic`, `Oem` |
| response | `Oem/Huawei/Public` | — |

### 4.4.29 加密盘的数据安全擦除（差异 3）

- BMC section: `3.4.40`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}/Actions/Oem/Huawei/Drive.CryptoErase`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/Drives/{drives_id}/Actions/Oem/Huawei/Public/Drive.CryptoErase`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `drive_id` | `drives_id` |
| header | `Content-Type` | — |

### 4.4.33 NPU模组复位（差异 3）

- BMC section: `3.4.44`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Boards/ACUBoard/Actions/NpuBoard.NpuBoardReset`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/Boards/{board_id}/Actions/NPUBoard.NPUBoardReset`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `board_id` |
| body | — | `DomainId` |
| response | — | `NPU模组复位信息` |

### 4.10.3.2 查询指定角色信息（差异 3）

- BMC section: `3.6.17`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/Roles/{role_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | — | `RoleId` |

### 4.10.9.1 查询Ldap服务资源（差异 3）

- BMC section: `3.6.21`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/LdapService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | — | `Ldap服务资源信息` |

### 4.10.9.2 修改Ldap功能开启使能（差异 3）

- BMC section: `3.6.22`  method: `PATCH`
- PoDM URI: `/redfish/v1/AccountService/LdapService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |
| response | — | `Ldap服务资源信息` |

### 4.10.9.3 查询Ldap域控制器集合信息（差异 3）

- BMC section: `3.6.23`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/LdapService/LdapControllers`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | — | `Ldap域控制器集合` |

### 4.5.3 查询指定可升级固件资源信息（差异 3）

- BMC section: `3.7.4`  method: `GET`
- PoDM URI: `/redfish/v1/UpdateService/FirmwareInventory/{softid}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `DeviceLocation`, `Oem/Huawei` | `Staged` |

### 4.9.17 提交测试指标报告上报（差异 3）

- BMC section: `3.15.17`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/Actions/TelemetryService.SubmitTestMetricReport`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `GeneratedMetricReportValues`, `MetricId` |
| response | — | `SubmitTestMetricReport资源信息` |

### 4.10.4.4 删除会话（差异 3）

- BMC section: `3.5.6`  method: `DELETE`
- PoDM URI: `/redfish/v1/SessionService/Sessions/{session_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |
| response | `@Message.ExtendedInfo` | — |

### 4.1.10 查询OData服务文档（差异 2）

- BMC section: `3.1.10`  method: `GET`
- PoDM URI: `/redfish/v1/{odata}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | — | `odata` |
| header | `X-Auth-Token` | — |

### 4.1.12 查询性能数据采集服务资源（差异 2）

- BMC section: `3.1.12`  method: `GET`
- PoDM URI: `/redfish/v1/PerformanceCollection`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `BladeN`, `ChassisId` | — |

### 4.3.11 查询虚拟媒体集合资源（差异 2）

- BMC section: `3.2.12`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VirtualMedia`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VirtualMedia`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |

### 4.3.6 查询VNC资源（差异 2）

- BMC section: `3.2.68`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/VncService`
- BMC URI: `/redfish/v1/Managers/{manager_id}/VncService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `system_id` | `manager_id` |

### 4.2.35 修改SP服务资源属性（差异 2）

- BMC section: `3.2.71`  method: `PATCH`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `ifmatch_value` | `If-Match` |

### 4.2.38 查询SP服务的OS安装配置集合资源（差异 2）

- BMC section: `3.2.76`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPOSInstallPara`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | — | `OS安装配置集合资源信息` |

### 4.2.53 创建SP服务的硬盘擦除配置（差异 2）

- BMC section: `3.2.91`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPDriveErase`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `DriveErase`, `EraseMode` |

### 4.2.96 查询PRBS测试信息（差异 2）

- BMC section: `3.2.158`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest/Actions/PRBSTest.QueryInfo`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | — |

### 4.2.98 清除PRBS测试统计（差异 2）

- BMC section: `3.2.160`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest/Actions/PRBSTest.ClearStatistics`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | — |

### 4.2.99 终止PRBS测试（差异 2）

- BMC section: `3.2.161`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/PRBSTest/Actions/PRBSTest.Shutdown`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |
| response | `Oem/Huawei` | — |

### 4.3.27 查询指定内存指标资源信息（差异 2）

- BMC section: `3.3.16`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Memory/{memory_id}/MemoryMetrics`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `MemoryMetrics.ClearCurrentPeriod`, `Oem/Huawei/Public` | — |

### 4.3.29 查询VLAN资源信息（差异 2）

- BMC section: `3.3.18`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/EthernetInterfaces/{ethernetinterface_id}/VLANs/{vlan_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | `VLAN资源信息` |

### 4.4.58 查询电子保单信息（差异 2）

- BMC section: `3.3.72`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/DigitalWarranty`
- BMC URI: `/redfish/v1/Systems/{system_id}/DigitalWarranty`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `chassis_id` | `system_id` |

### 4.4.5 恢复超节点配置信息为默认值（差异 2）

- BMC section: `3.4.6`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Oem/Huawei/Actions/Chassis.SuperPodLabelRestoreDefaults`
- BMC URI: `/redfish/v1/Chassis/Chassis_id/Oem/Huawei/Public/Actions/Chassis.SuperPodLabelRestoreDefaults`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `chassis_id` | — |
| header | `If-Match` | — |

### 4.4.22 查询网络端口单个资源信息（差异 2）

- BMC section: `3.4.28`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{networkadapters_id}/NetworkPorts/{networkports_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | `PortState` |

### 4.4.54 查询单个电源信息（差异 2）

- BMC section: `3.4.74`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/PowerSupplies/{PowerSupply_Id}`
- BMC URI: `/redfish/v1/Chassis/ChassisId/PowerSubsystem/PowerSupplies/PowerSupplyId`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `PowerSupply_Id`, `chassis_id` | — |

### 4.4.55 查询单个电源度量信息（差异 2）

- BMC section: `3.4.75`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PowerSubsystem/PowerSupplies/{PowerSupply_Id}/Metrics`
- BMC URI: `/redfish/v1/Chassis/ChassisId/PowerSubsystem/PowerSupplies/PowerSupplyId/Metrics`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `PowerSupply_Id`, `chassis_id` | — |

### 4.10.3.1 查询角色集合资源信息（差异 2）

- BMC section: `3.6.16`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/Roles`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |

### 4.10.9.4 查询具体域控制器的信息（差异 2）

- BMC section: `3.6.24`  method: `GET`
- PoDM URI: `/redfish/v1/AccountService/LdapService/LdapControllers/{member_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |

### 4.7.10 删除事件订阅资源（差异 2）

- BMC section: `3.9.10`  method: `DELETE`
- PoDM URI: `/redfish/v1/EventService/Subscriptions/{id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@Message.ExtendedInfo`, `RelatedProperties` |

### 4.7.11 屏蔽系统事件上报（差异 2）

- BMC section: `3.9.11`  method: `POST`
- PoDM URI: `/redfish/v1/EventService/Actions/Oem/Huawei/EventService.ShieldSystemAlert`
- BMC URI: `/redfish/v1/EventService/Actions/Oem/Huawei/Public/EventService.ShieldSystemAlert`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `@Message.ExtendedInfo`, `RelatedProperties` |

### 4.12.1 查询资源服务信息（差异 2）

- BMC section: `3.13.1`  method: `GET`
- PoDM URI: `/redfish/v1/Oem/Huawei/AssetService`
- BMC URI: `/redfish/v1/Oem/Huawei/Public/AssetService`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Links/TrustedSupplyChainChangedEvents` | `AssetService资源信息` |

### 4.9.6 创建指标报告定义资源信息（差异 2）

- BMC section: `3.15.6`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/MetricReportDefinitions`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `Metrics`, `Schedule` |

### 4.9.7 修改指定指标报告定义资源信息（差异 2）

- BMC section: `3.15.7`  method: `PATCH`
- PoDM URI: `/redfish/v1/TelemetryService/MetricReportDefinitions/{id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | — | `Metrics`, `Schedule` |

### 4.10.4.1 查询全量会话（差异 2）

- BMC section: `3.5.4`  method: `GET`
- PoDM URI: `/redfish/v1/SessionService/Sessions`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type`, `x-non-renewal-session` | — |

### 4.10.3.3 角色绑定权限（差异 2）

- BMC section: `3.6.18`  method: `PATCH`
- PoDM URI: `/redfish/v1/AccountService/Roles/{role_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `x-non-renewal-session` | `If-Match` |

### 4.9.18 清除指标报告（未开发）（差异 2）

- BMC section: `3.15.18`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/Actions/TelemetryService.ClearMetricReports`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `Content-Type` |
| response | — | `SubmitTestMetricReport资源信息` |

### 4.9.19 恢复指标报告定义到默认值 （未开发）（差异 2）

- BMC section: `3.15.19`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/Actions/TelemetryService.ResetMetricReportDefinitionsToDefaults`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `Content-Type` |
| response | — | `SubmitTestMetricReport资源信息` |

### 4.9.20 恢复触发器到默认值 (未开发)（差异 2）

- BMC section: `3.15.20`  method: `POST`
- PoDM URI: `/redfish/v1/TelemetryService/Actions/TelemetryService.ResetTriggersToDefaults`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `Content-Type` |
| response | — | `SubmitTestMetricReport资源信息` |

### 4.1.4 查询Metadata文档（差异 1）

- BMC section: `3.1.4`  method: `GET`
- PoDM URI: `/redfish/v1/$metadata`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `NA` | — |

### 4.2.82 下载BMC文件（差异 1）

- BMC section: `3.2.10`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager.GeneralDownload`
- BMC URI: `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/Manager.GeneralDownload`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `Path` | — |

### 4.2.7 SNMP发送测试事件（差异 1）

- BMC section: `3.2.26`  method: `POST`
- PoDM URI: `redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpService.SubmitTestEvent`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SnmpService/Actions/SnmpService.SubmitTestEvent`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SNMP发送测试事件信息` |

### 4.2.21 查询安全服务集合资源信息（差异 1）

- BMC section: `3.2.48`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SecurityService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `ComponentMeasurementPolicy` |

### 4.2.37 触发导出SP服务的RAID当前配置（差异 1）

- BMC section: `3.2.73`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Actions/SPService.ExportSPRAIDConfigurations`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.2.54 查询SP服务的硬盘擦除配置资源（差异 1）

- BMC section: `3.2.92`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPDriveErase/1`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SP服务的硬盘擦除配置资源的信息` |

### 4.2.55 查询SP系统擦除配置集合资源（差异 1）

- BMC section: `3.2.93`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SystemErase`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SP系统擦除配置集合配置资源的信息` |

### 4.2.57 查询指定SP系统擦除配置（差异 1）

- BMC section: `3.2.95`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SystemErase/{member_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SP系统擦除配置的信息` |

### 4.2.60 查询SP插件集合资源（差异 1）

- BMC section: `3.2.96`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Plugins`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SP插件集合资源信息` |

### 4.2.61 查询SP插件资源（差异 1）

- BMC section: `3.2.97`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/Plugins/{plugin_id}`
- BMC URI: `/redfish/v1/Managers/{manager_id}/SPService//Plugins/{plugin_id}`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `SP插件资源信息` |

### 4.2.88 停止录像回放（差异 1）

- BMC section: `3.2.102`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.StopVideoPlayback`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.2.71 删除截屏（差异 1）

- BMC section: `3.2.105`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/DiagnosticService/Actions/DiagnosticService.DeleteScreenShot`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.2.12 查询LLDP服务资源信息（差异 1）

- BMC section: `3.2.129`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/LldpService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `LLDP服务配置资源信息` |

### 4.2.111 查询USB管理服务资源信息（差异 1）

- BMC section: `3.2.134`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/USBMgmtService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `USB管理服务配置资源信息` |

### 4.2.92 查询FPCService服务资源（差异 1）

- BMC section: `3.2.136`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/FPCService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `FPCService资源的信息` |

### 4.2.58 创建SP服务的RAID配置（差异 1）

- BMC section: `3.2.141`  method: PoDM `GET` / BMC `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SPService/SPRAID`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `member_id` | — |

### 4.2.95 报废处置（差异 1）

- BMC section: `3.2.142`  method: `POST`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Manager.RetireSystem`
- BMC URI: `/redfish/v1/Managers/{manager_id}/Actions/Oem/Huawei/Public/Manager.RetireSystem`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.2.115 查询TPCM服务信息（差异 1）

- BMC section: `3.2.148`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/SecurityService/TpcmService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Tpcm服务配置资源信息` |

### 4.3.5 FRU上下电控制（差异 1）

- BMC section: `3.3.5`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Actions/Oem/Huawei/ComputerSystem.FruControl`
- BMC URI: `/redfish/v1/Systems/{system_id}/Actions/Oem/Huawei/Public/ComputerSystem.FruControl`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `FRU上下电控制信息` |

### 4.3.20 查询Bond集合资源信息（差异 1）

- BMC section: `3.3.9`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/NetworkBondings`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Bond集合资源信息` |

### 4.3.21 查询Bond资源信息（差异 1）

- BMC section: `3.3.10`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/NetworkBondings/{bond_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Bond资源信息` |

### 4.3.28 查询VLAN集合资源信息（差异 1）

- BMC section: `3.3.17`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/EthernetInterfaces/{ethernetinterface_id}/VLANs`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `VLAN集合资源信息` |

### 4.3.36 查询指定逻辑盘资源信息（差异 1）

- BMC section: `3.3.28`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Volumes/{volume_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | — |

### 4.3.43 修改BIOS密码（差异 1）

- BMC section: `3.3.35`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios/Actions/Bios.ChangePassword`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.3.44 查询BIOS设置资源信息（差异 1）

- BMC section: `3.3.36`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios/Settings`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei/Public` | — |

### 4.3.47 查询BIOS策略重配资源信息（差异 1）

- BMC section: `3.3.39`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Bios/PolicyConfig`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `BIOS策略重配属性列表` |

### 4.3.56 查询CPU历史占用率资源信息（差异 1）

- BMC section: `3.3.66`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/ProcessorsHistoryUsageRate`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `CPU历史占用率资源信息` |

### 4.3.62 导入Foreign配置（差异 1）

- BMC section: `3.3.74`  method: `POST`
- PoDM URI: `/redfish/v1/Systems/{system_id}/Storages/{storage_id}/Actions/Oem/Huawei/Public/Storage. ImportForeignConfig`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.3.63 查询IB集合资源信息（差异 1）

- BMC section: `3.3.76`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/InfiniBandInterfaces`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `IB集合资源信息` |

### 4.3.64 查询IB资源信息（差异 1）

- BMC section: `3.3.77`  method: `GET`
- PoDM URI: `/redfish/v1/Systems/{system_id}/InfiniBandInterfaces/{ib_id}`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `IB资源信息` |

### 4.4.12 重新统计功率数据（差异 1）

- BMC section: `3.4.13`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Actions/Power.ResetStatistics`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/Power/Oem/Huawei/Public/Actions/Power.ResetStatistics`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `@Message.ExtendedInfo` | — |

### 4.4.19 查询网络适配器集合资源信息（差异 1）

- BMC section: `3.4.18`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/NetworkAdapters`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | — |

### 4.4.34 查询PCIe设备集合资源信息（差异 1）

- BMC section: `3.4.46`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `PCIe设备集合资源信息` |

### 4.4.37 复位指定SDI卡（差异 1）

- BMC section: `3.4.49`  method: `POST`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}/Actions/Oem/Huawei/PCIeDevices.Reset`
- BMC URI: `/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pciedevices_id}/Actions/Oem/Huawei/Public/PCIeDevices.Reset`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | — | `Content-Type` |

### 4.4.56 查询Sensors集合资源（差异 1）

- BMC section: `3.4.69`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Sensors`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Sensors资源信息` |

### 4.4.57 查询指定Sensor资源信息（差异 1）

- BMC section: `3.4.70`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Sensors/{sensor_id}`
- BMC URI: `/ redfish/v1/Chassis/{chassis_id}/Sensors/{sensor_id}`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `sensor资源信息` |

### 4.6.1 查询任务服务资源信息（差异 1）

- BMC section: `3.8.1`  method: `GET`
- PoDM URI: `/redfish/v1/TaskService`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `TaskAutoDeleteTimeoutMinutes` |

### 4.6.5 查询指定子任务集合资源信息（差异 1）

- BMC section: `3.8.6`  method: `GET`
- PoDM URI: `/redfish/v1/TaskService/Tasks/{taskid}/SubTasks`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| path | `taskid` | — |

### 4.7.5 模拟精准告警（差异 1）

- BMC section: `3.9.5`  method: `POST`
- PoDM URI: `/redfish/v1/EventService/Actions/Oem/Huawei/EventService.MockPreciseAlarm`
- BMC URI: `/redfish/v1/EventService/Actions/Oem/Huawei/Public/EventService.MockPreciseAlarm`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| body | `BladeId` | — |

### 4.7.6 查询事件订阅集合资源（差异 1）

- BMC section: `3.9.6`  method: `GET`
- PoDM URI: `/redfish/v1/EventService/Subscriptions`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `EventService资源信息` |

### 4.12.2 查询硬件资产清单信息（差异 1）

- BMC section: `3.13.2`  method: `GET`
- PoDM URI: `/redfish/v1/Oem/Huawei/AssetService/AssetList`
- BMC URI: `/redfish/v1/Oem/Huawei/Public/AssetService/AssetList`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `AssetList资源信息` |

### 4.12.5 确认供应链配置检查信息（差异 1）

- BMC section: `3.13.5`  method: `POST`
- PoDM URI: `/redfish/v1/Oem/Huawei/AssetService/Actions/AssetService.ConfirmTrustedSupplyChain`
- BMC URI: `/redfish/v1/Oem/Huawei/Public/AssetService/Actions/AssetService.ConfirmTrustedSupplyChain`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| header | `Content-Type` | — |

### 4.9.11 查询指定指标报告资源信息（差异 1）

- BMC section: `3.15.11`  method: `GET`
- PoDM URI: `/redfish/v1/TelemetryService/MetricReports//{id}`
- BMC URI: `/redfish/v1/TelemetryService/MetricReports/{id}`  ← URI 不一致

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `Timestamp` |

### 4.2.18 查询PoDManager网卡集合信息（差异 1）

- BMC section: `3.2.41`  method: `GET`
- PoDM URI: `/redfish/v1/Managers/{manager_id}/EthernetInterfaces`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | — | `iBMCBMC网口集合资源信息` |

### 4.4.6 查询指定机柜散热资源信息（差异 1）

- BMC section: `3.4.7`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Thermal`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | — |

### 4.4.30 查询服务器扩展板卡集合资源信息（差异 1）

- BMC section: `3.4.41`  method: `GET`
- PoDM URI: `/redfish/v1/Chassis/{chassis_id}/Boards`

| 类别 | 仅 PoDM | 仅 BMC |
|---|---|---|
| response | `Oem/Huawei` | — |

## PoDManager 修订建议（按 BMC response 字段补充优先级）

> 列出所有 BMC 同名接口的 response 字段集合中、PoDM 没列出的字段。BMC 那边大多是真实响应数据，PoDM 漏列的字段大概率是 schema 表写漏。按缺失字段数降序。

### 全量 163 条（PoDM response 比 BMC 缺字段的接口）

| PoDM section | 标题 | 缺失数 | BMC 多出的 response 字段 |
|---|---|---:|---|
| 4.3.41 | 查询BIOS资源信息 | 1003 | `ADDDCEn`, `AESEnable`, `APDEn`, `APEIEinjType`, `APEISupport`, `ARIEnable`, `ATS`, `AcpiApicPolicy`, `AcpiHPETEnable`, `AcpiHpet`, `AcsEnable`, `ActiveCpuCores`, `AltEngPerfBIAS`, `ApdEn`, `AppDirectMemoryHole`, `ApplicationProfile`, `AttemptFastBootCold`, `Authority`, `AutoRefresh`, `AvxIccpLevel`, `BIOSSSABacksideMargining`, `BIOSSSACmdAll`, `BIOSSSACmdVref`, `BIOSSSACtlAll`, `BIOSSSADebugMessages`, `BIOSSSADisplayTables`, `BIOSSSAEarlyReadIdMargining`, `BIOSSSAEridDelay`, `BIOSSSAEridVref`, `BIOSSSALoopCount`, `BIOSSSAPerBitMargining`, `BIOSSSAPerDisplayPlots`, `BIOSSSARxDqs`, `BIOSSSARxVref`, `BIOSSSAStepSizeOverride`, `BIOSSSATxDq`, `BIOSSSATxVref`, `BIOS属性列表`, `BIOS资源信息`, `BMCWDTAction`, `BMCWDTEnable`, `BMCWDTTimeout`, `BenchMarkSelection`, `BiosSsaBacksideMargining`, `BiosSsaCmdAll`, `BiosSsaCmdVref`, `BiosSsaCtlAll`, `BiosSsaDebugMessages`, `BiosSsaDisplayTables`, `BiosSsaEarlyReadIdMargining`, `BiosSsaEridDelay`, `BiosSsaEridVref`, `BiosSsaLoopCount`, `BiosSsaPerBitMargining`, `BiosSsaPerDisplayPlots`, `BiosSsaRxDqs`, `BiosSsaRxVref`, `BiosSsaStepSizeOverride`, `BiosSsaTxDq`, `BiosSsaTxVref`, `BootFailPolicy`, `BootOverride`, `BootOverrideLegacy`, `BootOverrideUEFI`, `BootPState`, `BootRetry`, `BootType`, `BootTypeOrder0`, `BootTypeOrder1`, `BootTypeOrder2`, `BootTypeOrder2D`, `BootTypeOrder3`, `C6Enable`, `CAMargin`, `CKEIdleTimer`, `CKEProgramming`, `COMBaseAddress`, `CRAfterPost`, `CREnable`, `CRInfoWaitTime`, `CdnSupport`, `ChannelInterleaving`, `ChannelInterleaving_3Way`, `CheckCPUBIST`, `CkeIdleTimer`, `CkeProgramming`, `ClkGenSpreadSpectrumCheck`, `CoherencySupport`, `ColdBootFastSupport`, `ComBaseAddr`, `CompletionTimeout0`, `CompletionTimeout1`, `CompletionTimeout2`, `CompletionTimeout3`, `CompletionTimeout4`, `CompletionTimeout5`, `CompletionTimeout6`, `CompletionTimeout7`, `CompletionTimeoutValue0`, `CompletionTimeoutValue1`, `CompletionTimeoutValue2`, `CompletionTimeoutValue3`, `CompletionTimeoutValue4`, `CompletionTimeoutValue5`, `CompletionTimeoutValue6`, `CompletionTimeoutValue7`, `ConfigTDPLevel`, `ConfigTdpLock`, `CurrentUnderReport`, `CustomPowerPolicy`, `CustomRefreshRate`, `CustomRefreshRateEn`, `CustomizedFeatures`, `DCUIPPrefetcherEnable`, `DCUModeSelection`, `DCUStreamerPrefetcherEnable`, `DDRDebugLevel`, `DDRFreqLimit`, `DcpmmAveragePowerLimit`, `DcpmmEccModeSwitch`, `DcpmmMbbFeature`, `DcpmmMbbMaxPowerLimit`, `DdRefreshSupport`, `DdrFreqLimit`, `Degrade4SPreference`, `DemandScrubMode`, `DieInterleaving`, `DirectoryModeEn`, `DisableDirForAppDirect`, `DisplayMode`, `DramRaplEnable`, `DramRaplInit`, `EETurboDisable`, `EMCACSMIEn`, `EMCAEn`, `EadrSupport`, `EliminateDirectoryInFarMemory`, `EmcaCsmiEn`, `EmcaEn`, `EnableBIOSSSARMT`, `EnableBIOSSSARMTonFCB`, `EnableBiosSsaRMT`, `EnableBiosSsaRMTonFCB`, `EnableClockSpreadSpec`, `EnableProcHot`, `EnableThermalMonitor`, `EnableXE`, `EnableXe`, `EnforcePOR`, `ExecuteDisableBit`, `ExtendedType17`, `FDMSupport`, `FPKPortConfig0`, `FPKPortConfig1`, `FPKPortConfig2`, `FPKPortConfig3`, `FastGoConfig`, `FlowControl`, `FreqSelect`, `FrontPanelLock`, `GlobalBaudRate`, `GlobalDataBits`, `GlobalFlowControl`, `GlobalParity`, `GlobalStopBits`, `GlobalTerminalType`, `HWMemTest`, `IIOErrRegistersClearEn`, `IIOErrorEn`, `IMCInterleaving`, `IOAPICMode`, `IRQThreshold`, `ISOCEn`, `IioErrorPin0En`, `IioOOBMode`, `IntelSpeedSelectSupport`, `Interleave`, `InterruptRemap`, `Ipv4Pxe`, `Irq`, `IrqThreshold`, `IsocEn`, `KTIFailoverSMIEn`, `KTIPrefetchEn`, `KtiLinkL0pEn`, `KtiLinkL1En`, `KtiPrefetchEn`, `L2RfoPrefetchDisable`, `LLCDeadLineAlloc`, `LLCPrefetchEnable`, `LatchSystemShutdownState`, `LeakyBktHi`, `LeakyBktLo`, `LlcPrefetchEnable`, `LowOccupyControl`, `LpAsrMode`, `LsxImplementation`, `MCTPEn`, `MLCSpatialPrefetcherEnable`, `MLCStreamerPrefetcherEnable`, `MemCeFloodPolicy`, `MemInterleaveGran1LM`, `MemTestOnFastBoot`, `MemhotOutputOnlyOpt`, `MemhotSupport`, `MirrorMode`, `MlcSpatialPrefetcherEnable`, `MlcStreamerPrefetcherEnable`, `MmiohBase`, `MmiohSize`, `MonitorMWait`, `MonitorMwaitEnable`, `MultiSparingRanks`, `NetworkHttpsProtocol`, `NetworkProtocol`, `NgnArsOnBoot`, `NgnArsPublish`, `NgnAveragePower`, `NgnCmdTime`, `NgnEccRdChk`, `NgnThrottleTemp`, `NoBootReset`, `NumaEn`, `NvmQos`, `NvmdimmPerfConfig`, `NvmdimmPowerCyclePolicy`, `OSCx`, `OSWDTAction`, `OSWDTEnable`, `OSWDTTimeout`, `OemSecureBoot`, `OemTpmEnable`, `OnDieThermalThrottling`, `OsNativeAerSupport`, `OverclockingLock`, `PCHADREn`, `PCHPCIeGlobalASPM`, `PCHPCIeUX16MaxPayloadSize`, `PCHPCIeUX8MaxPayloadSize`, `PCHSATA`, `PCHSSATA`, `PCHUSBHSPort0`, `PCHUSBHSPort1`, `PCHUSBHSPort10`, `PCHUSBHSPort11`, `PCHUSBHSPort12`, `PCHUSBHSPort13`, `PCHUSBHSPort2`, `PCHUSBHSPort3`, `PCHUSBHSPort7`, `PCHUSBHSPort8`, `PCHUSBHSPort9`, `PCHUSBPerPortCtl`, `PCHUSBSSPort0`, `PCHUSBSSPort1`, `PCHUSBSSPort2`, `PCHUSBSSPort3`, `PCHUSBSSPort4`, `PCHUSBSSPort5`, `PCHUSBSSPort6`, `PCHUSBSSPort7`, `PCHUSBSSPort8`, `PCHUSBSSPort9`, `PCI64BitResourceAllocation`, `PCIeARISupport`, `PCIeGlobalASPM`, `PCIeLinkDis1`, `PCIeLinkDis10`, `PCIeLinkDis101`, `PCIeLinkDis105`, `PCIeLinkDis106`, `PCIeLinkDis107`, `PCIeLinkDis108`, `PCIeLinkDis109`, `PCIeLinkDis11`, `PCIeLinkDis110`, `PCIeLinkDis111`, `PCIeLinkDis112`, `PCIeLinkDis113`, `PCIeLinkDis114`, `PCIeLinkDis115`, `PCIeLinkDis116`, `PCIeLinkDis117`, `PCIeLinkDis118`, `PCIeLinkDis12`, `PCIeLinkDis122`, `PCIeLinkDis126`, `PCIeLinkDis127`, `PCIeLinkDis128`, `PCIeLinkDis129`, `PCIeLinkDis13`, `PCIeLinkDis130`, `PCIeLinkDis131`, `PCIeLinkDis132`, `PCIeLinkDis133`, `PCIeLinkDis134`, `PCIeLinkDis135`, `PCIeLinkDis136`, `PCIeLinkDis137`, `PCIeLinkDis138`, `PCIeLinkDis139`, `PCIeLinkDis143`, `PCIeLinkDis147`, `PCIeLinkDis148`, `PCIeLinkDis149`, `PCIeLinkDis150`, `PCIeLinkDis151`, `PCIeLinkDis152`, `PCIeLinkDis153`, `PCIeLinkDis154`, `PCIeLinkDis155`, `PCIeLinkDis156`, `PCIeLinkDis157`, `PCIeLinkDis158`, `PCIeLinkDis159`, `PCIeLinkDis160`, `PCIeLinkDis164`, `PCIeLinkDis17`, `PCIeLinkDis2`, `PCIeLinkDis21`, `PCIeLinkDis22`, `PCIeLinkDis23`, `PCIeLinkDis24`, `PCIeLinkDis25`, `PCIeLinkDis26`, `PCIeLinkDis27`, `PCIeLinkDis28`, `PCIeLinkDis29`, `PCIeLinkDis3`, `PCIeLinkDis30`, `PCIeLinkDis31`, `PCIeLinkDis32`, `PCIeLinkDis33`, `PCIeLinkDis34`, `PCIeLinkDis38`, `PCIeLinkDis4`, `PCIeLinkDis42`, `PCIeLinkDis43`, `PCIeLinkDis44`, `PCIeLinkDis45`, `PCIeLinkDis46`, `PCIeLinkDis47`, `PCIeLinkDis48`, `PCIeLinkDis49`, `PCIeLinkDis5`, `PCIeLinkDis50`, `PCIeLinkDis51`, `PCIeLinkDis52`, `PCIeLinkDis53`, `PCIeLinkDis54`, `PCIeLinkDis55`, `PCIeLinkDis59`, `PCIeLinkDis6`, `PCIeLinkDis63`, `PCIeLinkDis64`, `PCIeLinkDis65`, `PCIeLinkDis66`, `PCIeLinkDis67`, `PCIeLinkDis68`, `PCIeLinkDis69`, `PCIeLinkDis7`, `PCIeLinkDis70`, `PCIeLinkDis71`, `PCIeLinkDis72`, `PCIeLinkDis73`, `PCIeLinkDis74`, `PCIeLinkDis75`, `PCIeLinkDis76`, `PCIeLinkDis8`, `PCIeLinkDis80`, `PCIeLinkDis84`, `PCIeLinkDis85`, `PCIeLinkDis86`, `PCIeLinkDis87`, `PCIeLinkDis88`, `PCIeLinkDis89`, `PCIeLinkDis9`, `PCIeLinkDis90`, `PCIeLinkDis91`, `PCIeLinkDis92`, `PCIeLinkDis93`, `PCIeLinkDis94`, `PCIeLinkDis95`, `PCIeLinkDis96`, `PCIeLinkDis97`, `PCIePortDisable1`, `PCIePortDisable10`, `PCIePortDisable101`, `PCIePortDisable105`, `PCIePortDisable106`, `PCIePortDisable107`, `PCIePortDisable108`, `PCIePortDisable109`, `PCIePortDisable11`, `PCIePortDisable110`, `PCIePortDisable111`, `PCIePortDisable112`, `PCIePortDisable113`, `PCIePortDisable114`, `PCIePortDisable115`, `PCIePortDisable116`, `PCIePortDisable117`, `PCIePortDisable118`, `PCIePortDisable12`, `PCIePortDisable122`, `PCIePortDisable126`, `PCIePortDisable127`, `PCIePortDisable128`, `PCIePortDisable129`, `PCIePortDisable13`, `PCIePortDisable130`, `PCIePortDisable131`, `PCIePortDisable132`, `PCIePortDisable133`, `PCIePortDisable134`, `PCIePortDisable135`, `PCIePortDisable136`, `PCIePortDisable137`, `PCIePortDisable138`, `PCIePortDisable139`, `PCIePortDisable143`, `PCIePortDisable147`, `PCIePortDisable148`, `PCIePortDisable149`, `PCIePortDisable150`, `PCIePortDisable151`, `PCIePortDisable152`, `PCIePortDisable153`, `PCIePortDisable154`, `PCIePortDisable155`, `PCIePortDisable156`, `PCIePortDisable157`, `PCIePortDisable158`, `PCIePortDisable159`, `PCIePortDisable160`, `PCIePortDisable164`, `PCIePortDisable17`, `PCIePortDisable2`, `PCIePortDisable21`, `PCIePortDisable22`, `PCIePortDisable23`, `PCIePortDisable24`, `PCIePortDisable25`, `PCIePortDisable26`, `PCIePortDisable27`, `PCIePortDisable28`, `PCIePortDisable29`, `PCIePortDisable3`, `PCIePortDisable30`, `PCIePortDisable31`, `PCIePortDisable32`, `PCIePortDisable33`, `PCIePortDisable34`, `PCIePortDisable38`, `PCIePortDisable4`, `PCIePortDisable42`, `PCIePortDisable43`, `PCIePortDisable44`, `PCIePortDisable45`, `PCIePortDisable46`, `PCIePortDisable47`, `PCIePortDisable48`, `PCIePortDisable49`, `PCIePortDisable5`, `PCIePortDisable50`, `PCIePortDisable51`, `PCIePortDisable52`, `PCIePortDisable53`, `PCIePortDisable54`, `PCIePortDisable55`, `PCIePortDisable59`, `PCIePortDisable6`, `PCIePortDisable63`, `PCIePortDisable64`, `PCIePortDisable65`, `PCIePortDisable66`, `PCIePortDisable67`, `PCIePortDisable68`, `PCIePortDisable69`, `PCIePortDisable7`, `PCIePortDisable70`, `PCIePortDisable71`, `PCIePortDisable72`, `PCIePortDisable73`, `PCIePortDisable74`, `PCIePortDisable75`, `PCIePortDisable76`, `PCIePortDisable8`, `PCIePortDisable80`, `PCIePortDisable84`, `PCIePortDisable85`, `PCIePortDisable86`, `PCIePortDisable87`, `PCIePortDisable88`, `PCIePortDisable89`, `PCIePortDisable9`, `PCIePortDisable90`, `PCIePortDisable91`, `PCIePortDisable92`, `PCIePortDisable93`, `PCIePortDisable94`, `PCIePortDisable95`, `PCIePortDisable96`, `PCIePortDisable97`, `PCIePortLinkSpeed1`, `PCIePortLinkSpeed10`, `PCIePortLinkSpeed101`, `PCIePortLinkSpeed105`, `PCIePortLinkSpeed106`, `PCIePortLinkSpeed107`, `PCIePortLinkSpeed108`, `PCIePortLinkSpeed109`, `PCIePortLinkSpeed11`, `PCIePortLinkSpeed110`, `PCIePortLinkSpeed111`, `PCIePortLinkSpeed112`, `PCIePortLinkSpeed113`, `PCIePortLinkSpeed114`, `PCIePortLinkSpeed115`, `PCIePortLinkSpeed116`, `PCIePortLinkSpeed117`, `PCIePortLinkSpeed118`, `PCIePortLinkSpeed12`, `PCIePortLinkSpeed122`, `PCIePortLinkSpeed126`, `PCIePortLinkSpeed127`, `PCIePortLinkSpeed128`, `PCIePortLinkSpeed129`, `PCIePortLinkSpeed13`, `PCIePortLinkSpeed130`, `PCIePortLinkSpeed131`, `PCIePortLinkSpeed132`, `PCIePortLinkSpeed133`, `PCIePortLinkSpeed134`, `PCIePortLinkSpeed135`, `PCIePortLinkSpeed136`, `PCIePortLinkSpeed137`, `PCIePortLinkSpeed138`, `PCIePortLinkSpeed139`, `PCIePortLinkSpeed143`, `PCIePortLinkSpeed147`, `PCIePortLinkSpeed148`, `PCIePortLinkSpeed149`, `PCIePortLinkSpeed150`, `PCIePortLinkSpeed151`, `PCIePortLinkSpeed152`, `PCIePortLinkSpeed153`, `PCIePortLinkSpeed154`, `PCIePortLinkSpeed155`, `PCIePortLinkSpeed156`, `PCIePortLinkSpeed157`, `PCIePortLinkSpeed158`, `PCIePortLinkSpeed159`, `PCIePortLinkSpeed160`, `PCIePortLinkSpeed164`, `PCIePortLinkSpeed17`, `PCIePortLinkSpeed2`, `PCIePortLinkSpeed21`, `PCIePortLinkSpeed22`, `PCIePortLinkSpeed23`, `PCIePortLinkSpeed24`, `PCIePortLinkSpeed25`, `PCIePortLinkSpeed26`, `PCIePortLinkSpeed27`, `PCIePortLinkSpeed28`, `PCIePortLinkSpeed29`, `PCIePortLinkSpeed3`, `PCIePortLinkSpeed30`, `PCIePortLinkSpeed31`, `PCIePortLinkSpeed32`, `PCIePortLinkSpeed33`, `PCIePortLinkSpeed34`, `PCIePortLinkSpeed38`, `PCIePortLinkSpeed4`, `PCIePortLinkSpeed42`, `PCIePortLinkSpeed43`, `PCIePortLinkSpeed44`, `PCIePortLinkSpeed45`, `PCIePortLinkSpeed46`, `PCIePortLinkSpeed47`, `PCIePortLinkSpeed48`, `PCIePortLinkSpeed49`, `PCIePortLinkSpeed5`, `PCIePortLinkSpeed50`, `PCIePortLinkSpeed51`, `PCIePortLinkSpeed52`, `PCIePortLinkSpeed53`, `PCIePortLinkSpeed54`, `PCIePortLinkSpeed55`, `PCIePortLinkSpeed59`, `PCIePortLinkSpeed6`, `PCIePortLinkSpeed63`, `PCIePortLinkSpeed64`, `PCIePortLinkSpeed65`, `PCIePortLinkSpeed66`, `PCIePortLinkSpeed67`, `PCIePortLinkSpeed68`, `PCIePortLinkSpeed69`, `PCIePortLinkSpeed7`, `PCIePortLinkSpeed70`, `PCIePortLinkSpeed71`, `PCIePortLinkSpeed72`, `PCIePortLinkSpeed73`, `PCIePortLinkSpeed74`, `PCIePortLinkSpeed75`, `PCIePortLinkSpeed76`, `PCIePortLinkSpeed8`, `PCIePortLinkSpeed80`, `PCIePortLinkSpeed84`, `PCIePortLinkSpeed85`, `PCIePortLinkSpeed86`, `PCIePortLinkSpeed87`, `PCIePortLinkSpeed88`, `PCIePortLinkSpeed89`, `PCIePortLinkSpeed9`, `PCIePortLinkSpeed90`, `PCIePortLinkSpeed91`, `PCIePortLinkSpeed92`, `PCIePortLinkSpeed93`, `PCIePortLinkSpeed94`, `PCIePortLinkSpeed95`, `PCIePortLinkSpeed96`, `PCIePortLinkSpeed97`, `PCIeRootPortASPM0`, `PCIeRootPortASPM1`, `PCIeRootPortASPM10`, `PCIeRootPortASPM11`, `PCIeRootPortASPM12`, `PCIeRootPortASPM13`, `PCIeRootPortASPM14`, `PCIeRootPortASPM15`, `PCIeRootPortASPM16`, `PCIeRootPortASPM17`, `PCIeRootPortASPM18`, `PCIeRootPortASPM19`, `PCIeRootPortASPM2`, `PCIeRootPortASPM3`, `PCIeRootPortASPM6`, `PCIeRootPortASPM7`, `PCIeRootPortASPM8`, `PCIeRootPortASPM9`, `PCIeRootPortEn0`, `PCIeRootPortEn1`, `PCIeRootPortEn10`, `PCIeRootPortEn11`, `PCIeRootPortEn12`, `PCIeRootPortEn13`, `PCIeRootPortEn14`, `PCIeRootPortEn15`, `PCIeRootPortEn16`, `PCIeRootPortEn17`, `PCIeRootPortEn18`, `PCIeRootPortEn19`, `PCIeRootPortEn2`, `PCIeRootPortEn3`, `PCIeRootPortEn6`, `PCIeRootPortEn7`, `PCIeRootPortEn8`, `PCIeRootPortEn9`, `PCIeRootPortMSIE0`, `PCIeRootPortMSIE1`, `PCIeRootPortMSIE10`, `PCIeRootPortMSIE11`, `PCIeRootPortMSIE12`, `PCIeRootPortMSIE13`, `PCIeRootPortMSIE14`, `PCIeRootPortMSIE15`, `PCIeRootPortMSIE16`, `PCIeRootPortMSIE17`, `PCIeRootPortMSIE18`, `PCIeRootPortMSIE19`, `PCIeRootPortMSIE2`, `PCIeRootPortMSIE3`, `PCIeRootPortMSIE6`, `PCIeRootPortMSIE7`, `PCIeRootPortMSIE8`, `PCIeRootPortMSIE9`, `PCIeRootPortMaxPayLoadSize0`, `PCIeRootPortMaxPayLoadSize1`, `PCIeRootPortMaxPayLoadSize10`, `PCIeRootPortMaxPayLoadSize11`, `PCIeRootPortMaxPayLoadSize12`, `PCIeRootPortMaxPayLoadSize13`, `PCIeRootPortMaxPayLoadSize14`, `PCIeRootPortMaxPayLoadSize15`, `PCIeRootPortMaxPayLoadSize16`, `PCIeRootPortMaxPayLoadSize17`, `PCIeRootPortMaxPayLoadSize18`, `PCIeRootPortMaxPayLoadSize19`, `PCIeRootPortMaxPayLoadSize2`, `PCIeRootPortMaxPayLoadSize3`, `PCIeRootPortMaxPayLoadSize6`, `PCIeRootPortMaxPayLoadSize7`, `PCIeRootPortMaxPayLoadSize8`, `PCIeRootPortMaxPayLoadSize9`, `PCIeRootPortSpeed0`, `PCIeRootPortSpeed1`, `PCIeRootPortSpeed10`, `PCIeRootPortSpeed11`, `PCIeRootPortSpeed12`, `PCIeRootPortSpeed13`, `PCIeRootPortSpeed14`, `PCIeRootPortSpeed15`, `PCIeRootPortSpeed16`, `PCIeRootPortSpeed17`, `PCIeRootPortSpeed18`, `PCIeRootPortSpeed19`, `PCIeRootPortSpeed2`, `PCIeRootPortSpeed3`, `PCIeRootPortSpeed6`, `PCIeRootPortSpeed7`, `PCIeRootPortSpeed8`, `PCIeRootPortSpeed9`, `PCIeSRIOVSupport`, `PCIeTopology0`, `PCIeTopology1`, `PCIeTopology10`, `PCIeTopology11`, `PCIeTopology12`, `PCIeTopology13`, `PCIeTopology14`, `PCIeTopology15`, `PCIeTopology16`, `PCIeTopology17`, `PCIeTopology18`, `PCIeTopology19`, `PCIeTopology2`, `PCIeTopology3`, `PCIeTopology6`, `PCIeTopology7`, `PCIeTopology8`, `PCIeTopology9`, `POSTBootWDTimerPolicy`, `POSTBootWDTimerTimeout`, `PPDEn`, `PStateDomain`, `PXE1Setting`, `PXE2Setting`, `PXE3Setting`, `PXE4Setting`, `PXE5Setting`, `PXE6Setting`, `PXE7Setting`, `PXE8Setting`, `PXEBootToLan`, `PXEBootToLanLegacy`, `PXEBootToLanUEFI`, `PXEOnly`, `PackageCState`, `PagePolicy`, `PartialMirrorSAD0`, `PartialMirrorUefi`, `PartialMirrorUefiPercent`, `PassThroughDMA`, `PatrolScrub`, `PatrolScrubDuration`, `PchBackUsbPort1`, `PchBackUsbPort2`, `PchBackUsbPort3`, `PchBackUsbPort4`, `PchFrontUsbPort1`, `PchFrontUsbPort2`, `PchFrontUsbPort3`, `PchFrontUsbPort4`, `PchInternalUsbPort1`, `PchInternalUsbPort2`, `PchPcieUX16MaxPayloadSize`, `PchPcieUX8MaxPayloadSize`, `PchSata`, `PchUsbDegradeBar`, `PchsSata`, `Pci64BitResourceAllocation`, `PcieAerEcrcEn`, `PcieAerSurpriseLinkDownEn`, `PcieAerUreEn`, `PcieDmiAspm`, `PciePortPolicy`, `PcieRelaxedOrdering`, `PerformanceTuningMode`, `Persistent`, `PkgCLatNeg`, `PlusOneEn`, `PmemCaching`, `PoisonEn`, `PostedInterrupt`, `PowerOnPassword`, `PowerSaving`, `PpdEn`, `ProcessorActiveCore`, `ProcessorActivePbf`, `ProcessorAutonomousCStateEnable`, `ProcessorAutonomousCstateEnable`, `ProcessorC1eEnable`, `ProcessorConfigurePbf`, `ProcessorEISTEnable`, `ProcessorEISTPSDFunc`, `ProcessorEPPEnable`, `ProcessorEPPProfile`, `ProcessorEistEnable`, `ProcessorEistPsdFunc`, `ProcessorEppProfile`, `ProcessorFlexibleRatio`, `ProcessorFlexibleRatioOverrideEnable`, `ProcessorHWPMEnable`, `ProcessorHWPMInterrupt`, `ProcessorHyperThreading`, `ProcessorHyperThreadingDisable`, `ProcessorLTSXEnable`, `ProcessorLtsxEnable`, `ProcessorOutofBandAlternateEPB`, `ProcessorRaplPrioritization`, `ProcessorSPD`, `ProcessorSinglePCTLEn`, `ProcessorVMXEnable`, `ProcessorVmxEnable`, `ProcessorX2APIC`, `ProcessorX2apic`, `ProchotResponseRatio`, `PwrPerfTuning`, `PxeBootToLan`, `PxeRetryCount`, `PxeRetrylimites`, `PxeTimeoutRetryControl`, `QpiLinkSpeed`, `QuickBoot`, `QuietBoot`, `RMTOnColdFastBoot`, `RMTPatternLength`, `RankInterleaving`, `RankMargin`, `RankSparing`, `RdtCatOpportunisticTuning`, `ResetAndEraseToAllNVDimm`, `RestoreNVDIMMS`, `Rrq`, `SATAAlternateID`, `SATAExternal0`, `SATAExternal1`, `SATAExternal2`, `SATAExternal3`, `SATAExternal4`, `SATAExternal5`, `SATAExternal6`, `SATAExternal7`, `SATAHotPlug0`, `SATAHotPlug1`, `SATAHotPlug2`, `SATAHotPlug3`, `SATAHotPlug4`, `SATAHotPlug5`, `SATAHotPlug6`, `SATAHotPlug7`, `SATAInterfaceMode`, `SATAPort0`, `SATAPort1`, `SATAPort2`, `SATAPort3`, `SATAPort4`, `SATAPort5`, `SATAPort6`, `SATAPort7`, `SATARAIDLoadEFIDriver`, `SATATopology0`, `SATATopology1`, `SATATopology2`, `SATATopology3`, `SATATopology4`, `SATATopology5`, `SATATopology6`, `SATATopology7`, `SATAType0`, `SATAType1`, `SATAType2`, `SATAType3`, `SATAType4`, `SATAType5`, `SATAType6`, `SATAType7`, `SNCEn`, `SPBoot`, `SSATAAlternateID`, `SSATAExternal0`, `SSATAExternal1`, `SSATAExternal2`, `SSATAExternal3`, `SSATAExternal4`, `SSATAExternal5`, `SSATAHotPlug0`, `SSATAHotPlug1`, `SSATAHotPlug2`, `SSATAHotPlug3`, `SSATAHotPlug4`, `SSATAHotPlug5`, `SSATAInterfaceMode`, `SSATAPort0`, `SSATAPort1`, `SSATAPort2`, `SSATAPort3`, `SSATAPort4`, `SSATAPort5`, `SSATARAIDLoadEFIDriver`, `SSATATopology0`, `SSATATopology1`, `SSATATopology2`, `SSATATopology3`, `SSATATopology4`, `SSATATopology5`, `SSATAType0`, `SSATAType1`, `SSATAType2`, `SSATAType3`, `SSATAType4`, `SSATAType5`, `SataInterfaceMode`, `SecureBoot`, `SerialDebugMsgLvl`, `SimplePassWord`, `Slot1PXESetting`, `Slot2PXESetting`, `Slot3PXESetting`, `Slot4PXESetting`, `Slot5PXESetting`, `Slot6PXESetting`, `Slot7PXESetting`, `Slot8PXESetting`, `SlotPxeDis`, `SlotPxeEnable`, `SncEn`, `SocketInterleaveBelow4GB`, `SpareErrTh`, `SpdDataRepair`, `SpsAltitude`, `SriovEnablePolicy`, `StaleAtoSOptEn`, `StaticTurbo`, `Support40Bit`, `Support44Bit`, `SupportOSCtrlAER`, `SysDBGLevel`, `SystemCpuUsage`, `SystemErrorEn`, `SystemPcieGlobalAspm`, `SystemVMDConfigEnable`, `TCCActivationOffset`, `TStateEnable`, `TcoTimeout`, `Thermalmemtrip`, `Thermalthrottlingsupport`, `TpmAvailability`, `TurboMode`, `TurboPowerLimitLock`, `TurboRatioLimitCores0`, `TurboRatioLimitCores1`, `TurboRatioLimitCores2`, `TurboRatioLimitCores3`, `TurboRatioLimitCores4`, `TurboRatioLimitCores5`, `TurboRatioLimitCores6`, `TurboRatioLimitCores7`, `TurboRatioLimitRatio0`, `TurboRatioLimitRatio1`, `TurboRatioLimitRatio2`, `TurboRatioLimitRatio3`, `TurboRatioLimitRatio4`, `TurboRatioLimitRatio5`, `TurboRatioLimitRatio6`, `TurboRatioLimitRatio7`, `UFSDisable`, `USBBoot`, `USBPrecondition`, `UefiPXE1Setting`, `UefiPXE2Setting`, `UefiPXE3Setting`, `UefiPXE4Setting`, `VMDConfigEnable`, `VTdSupport`, `VideoSelect`, `WHEALogMemoryEn`, `WHEALogPCIEn`, `WHEALogProcEn`, `WHEASupportEn`, `WakeOnPME`, `WakeOnS5`, `WakeOnS5DayOfMonth`, `WarmBootFastSupport`, `WheaLogMemoryEn`, `WheaLogPciEn`, `WheaLogProcEn`, `WheaSupportEn`, `XHCIDisMSICapability`, `XHCIOCMapEnabled`, `XHCIWakeOnUsbEnabled`, `XPTPrefetchEn`, `XptPrefetchEn`, `leakyBktHour`, `leakyBktMinute`, `partialmirrorsad0`, `refreshMode`, `sSataInterfaceMode`, `serialDebugMsgLvl`, `spareErrTh`, `thermalthrottlingsupport`, `volMemMode` |
| 4.4.2 | 查询指定机柜资源信息 | 56 | `AssetOwner`, `AvailableRackSpaceU`, `BackupBatteryUnits`, `BasicRackSN`, `Board`, `Building`, `BunchId`, `BunchType`, `CabinetSerialNumber`, `Chassis`, `ChassisLocation`, `CheckInTime`, `City`, `ContainedBy`, `Country`, `DepthMm`, `DeviceType`, `Direction`, `DirectionType`, `DiscoveredTime`, `EmptyRackSN`, `ExtendField`, `Floor`, `HeightMm`, `HouseNumber`, `IndicatorColor`, `InfoFormat`, `LifeCycleYear`, `LoadCapacityKg`, `ManufacturingDate`, `MezzCardNum`, `Placement`, `PostalAddress`, `PostalCode`, `Presence`, `Processors`, `ProductName`, `RFIDTagUID`, `RWCapability`, `Rack`, `RackModel`, `RatedPowerWatts`, `Room`, `Row`, `SDCardNum`, `SDContollerNum`, `Street`, `Territory`, `TopUSlot`, `TotalUCount`, `Type`, `UHeight`, `UcountUsed`, `UnitOccupyDirection`, `WeightKg`, `WidthMm` |
| 4.2.46 | 查询SP服务的配置结果资源 | 55 | `Aborted`, `ActualTestResult`, `AssetVerification`, `CPUID`, `CPU详细信息`, `Cancelled`, `Cancelling`, `Capacity`, `ClockSpeed`, `Completed`, `CountItem`, `CountVerification`, `DeviceName`, `DiagnoseMessage`, `DiagnoseResult`, `Diagnosing`, `DignoseResult`, `Executing`, `ExpectedTestResult`, `Failed`, `Finished`, `Firmware`, `Interrupted`, `MaxPower`, `Metrics`, `NPU详细信息`, `PartNumber`, `Pending`, `Position`, `Power详细信息`, `Qty`, `Reason`, `Reasons`, `RebootDelayMinutes`, `Result`, `ResultRaw`, `Running`, `Stopping`, `Successful`, `Suggestion`, `TaskList`, `TaskName`, `TaskState任务状态说明`, `Threshold`, `Type`, `Value`, `Waiting`, `decrypt_failed`, `encrypt_failed`, `network_failed`, `process_failed`, `progressing`, `successful`, `trans_failed`, `upload_failed` |
| 4.10.2.1 | 查询账户策略 | 49 | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `CertificateRevocationCheckEnabled`, `Certificates`, `CrlValidFrom`, `CrlValidTo`, `CrlVerificationEnabled`, `EmergencyLoginUser`, `Enabled`, `HTTPBasicAuth`, `InterChassisAuthentication`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KerberosService`, `KeyUsage`, `LdapService`, `LocalAccountAuth`, `LocalRole`, `OSAdministratorPrivilegeEnabled`, `OSUserManagementEnabled`, `PasswordExpirationDays`, `PasswordPattern`, `PasswordRulePolicy`, `PublicKeyLengthBits`, `RemoteGroup`, `RemoteRoleMapping`, `RequireChangePasswordAction`, `RootCertificate`, `SSHPasswordAuthenticationEnabled`, `SerialNumber`, `SignatureAlgorithm`, `Status`, `SystemLockDownEnabled`, `TwoFactorAuthenticationInformation`, `TwoFactorAuthenticationStateEnabled`, `UsernamePasswordCompareEnabled`, `UsernamePasswordCompareInfo`, `UsernamePasswordCompareLength`, `ValidFrom`, `ValidTo`, `target` |
| 4.10.2.2 | 修改账户策略 | 46 | `@Redfish.ActionInfo`, `AccessRole`, `AccountLockoutCounterResetAfter`, `AccountService资源信息`, `AuthFailureLoggingThreshold`, `Authentication`, `AuthenticationType`, `CLISessionTimeoutMinutes`, `CertId`, `Certificates`, `CrlValidFrom`, `CrlValidTo`, `EmergencyLoginUser`, `Enabled`, `HTTPBasicAuth`, `InitialAccountPrivilegeRestrictEnabled`, `InterChassisAuthentication`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KerberosService`, `KeyUsage`, `LdapService`, `LocalAccountAuth`, `LocalRole`, `OSUserManagementEnabled`, `PasswordExpirationDays`, `PasswordPattern`, `PasswordRulePolicy`, `PublicKeyLengthBits`, `RemoteGroup`, `RemoteRoleMapping`, `RequireChangePasswordAction`, `RootCertificate`, `SSHPasswordAuthenticationEnabled`, `SerialNumber`, `SignatureAlgorithm`, `Status`, `SystemLockDownEnabled`, `TwoFactorAuthenticationInformation`, `UsernamePasswordCompareEnabled`, `UsernamePasswordCompareInfo`, `UsernamePasswordCompareLength`, `ValidFrom`, `ValidTo`, `target` |
| 4.7.7 | 创建事件订阅资源 | 31 | `@Redfish.ActionInfo`, `@odata.context`, `@odata.id`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `Context`, `DeliveryRetryPolicy`, `Destination`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `EventTypes`, `HttpHeaders`, `Id`, `MessageIds`, `Name`, `OriginResources`, `Protocol`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |
| 4.1.2 | 查询当前根服务资源 | 27 | `ComponentIntegrity`, `DeepOperations`, `DeepPATCH`, `DeepPOST`, `ExcerptQuery`, `ExpandAll`, `ExpandQuery`, `Fabrics`, `FilterQuery`, `FilterQueryComparisonOperations`, `FilterQueryCompoundOperations`, `JobService`, `LCNService`, `Levels`, `Links`, `MaxLevels`, `NoLinks`, `ObservabilityService`, `OnlyMemberQuery`, `Product`, `ProtocolFeaturesSupported`, `SelectQuery`, `StartupDurationSeconds`, `StartupState`, `TelemetryService`, `TopSkipQuery`, `Vendor` |
| 4.7.3 | 模拟测试事件 | 25 | `@odata.context`, `@odata.id`, `Addinfo`, `Context`, `EventId`, `EventSubject`, `EventTimestamp`, `EventType`, `Events`, `Id`, `Level`, `Name`, `OriginOfCondition`, `ServerIdentity`, `ServerLocation`, `alarmStatus`, `locationInfo`, `neName`, `neType`, `neUID`, `objectName`, `objectType`, `objectUID`, `specificProblem`, `specificProblemID` |
| 4.2.19 | 查询PoDManager指定网卡信息 | 24 | `AdaptiveFlag`, `AdaptivePort`, `Chassis`, `ChassisLanSubNet`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link`, `Links`, `ManagementNetworkPort`, `ManagementNetworkPort@Redfish.AllowableValues`, `ManagementNetworkPortMembers`, `NetworkPortMode`, `OperatingMode`, `PortNumber`, `StaticNameServers`, `SwitchConnectionPortIDs`, `SwitchConnections`, `SwitchManagementIP`, `Type`, `UseNTPServers`, `VLAN` |
| 4.2.16 | 查询PoDManager服务信息 | 23 | `AccessMode`, `Certificates`, `Certificates.@odata.id`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `FQDN`, `HideCommunityStrings`, `HostName`, `HttpProtocolVersion`, `NTPServers`, `NetworkSuppliedServers`, `NotifyEnabled`, `NotifyIPv6Scope`, `NotifyMulticastIntervalSeconds`, `NotifyTTL`, `Port1`, `Port2`, `RMCPEnabled`, `RMCPPlusEnabled`, `iBMCBMC服务集合资源信息` |
| 4.3.2 | 查询指定系统资源信息 | 22 | `ActivatedSessionsType`, `AutoOSLockEnabled`, `AutoOSLockKey`, `AutoOSLockType`, `BSasCtrlSdkVersion`, `BWUWaveTitle`, `DelaySecondsAfterCpuThermalTrip`, `DisableKeyboardDuringBiosStartup`, `EnergySavingEnabled`, `HotSpare`, `KVMSettings`, `MaximumNumberOfSessions`, `NumberOfActiveSessions`, `PersistentUSBConnectionEnabled`, `PowerMode`, `PowerOnAfterCpuThermalTrip`, `SSDMediaLifeLeftPercentThreshold`, `SecureBoot`, `Spans`, `VirtualMedia`, `VncSettings`, `Volumes` |
| 4.7.8 | 查询事件订阅资源 | 21 | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `OriginResources`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |
| 4.7.9 | 修改事件订阅资源 | 21 | `@Redfish.ActionInfo`, `Actions`, `AuthenticationKey`, `AuthenticationKeySet`, `AuthenticationProtocol`, `DeliveryRetryPolicy`, `EncryptionKey`, `EncryptionKeySet`, `EncryptionProtocol`, `EventDestination.ResumeSubscription`, `EventDestination.SuspendSubscription`, `EventFormatType`, `OriginResources`, `SNMP`, `ServerIdentity`, `Severities`, `Status`, `SubscriptionType`, `TrapCommunity`, `TrapMode`, `target` |
| 4.2.20 | 修改指定PoDManager网卡信息 | 20 | `AdaptiveFlag`, `AdaptivePort`, `DHCPEnabled`, `DHCPv4`, `DHCPv6`, `EthernetInterface`, `IPv6Enabled`, `Link`, `ManagementNetworkPort`, `ManagementNetworkPort@Redfish.AllowableValues`, `ManagementNetworkPortMembers`, `NetworkPortMode`, `OperatingMode`, `SpeedMbps`, `StaticNameServers`, `SwitchConnectionPortIDs`, `SwitchConnections`, `SwitchManagementIP`, `UseNTPServers`, `VLAN` |
| 4.2.4 | 查看SNMP资源信息 | 19 | `@Redfish.ActionInfo`, `Actions`, `BobEnabled`, `Links`, `LoginRule`, `LongPasswordEnabled`, `PasswordPattern`, `PasswordRulePolicy`, `RWCommunityEnabled`, `ReadOnlyCommunity`, `ReadWriteCommunity`, `SNMP资源信息`, `SnmpV1Enabled`, `SnmpV2CEnabled`, `SnmpV3Enabled`, `SystemContact`, `SystemLocation`, `TrapMode`, `target` |
| 4.10.1.4 | 查询全量用户 | 19 | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `KeyUsage`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `PublicKeyLengthBits`, `RevokedDate`, `RevokedState`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo`, `target` |
| 4.5.1 | 查询升级服务资源信息 | 18 | `@Redfish.ActionInfo`, `AutoFirmwareActivationEnable`, `CertificateRevocationLists`, `Certificates`, `FirmwareIntegrity`, `FirmwareToTakeEffect`, `FirmwareType`, `InbandFirmwareUpdateEnabled`, `MaxImageSizeBytes`, `RelatedFirmwareItems`, `StagedTime`, `StagedVersion`, `SyncUpdateState`, `Task`, `UpdateService.ActivateBios`, `UpdateService.SimpleUpdate`, `UpdateService.StartActivate`, `UpdateService.StartSyncUpdate` |
| 4.10.1.2 | 修改用户 | 17 | `@Redfish.ActionInfo`, `FingerPrint`, `IssueBy`, `IssueTo`, `LastLoginInterface`, `LastLoginIp`, `LastLoginTime`, `LoginAudit`, `RevokedDate`, `RevokedState`, `Roles`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `ValidFrom`, `ValidTo`, `target` |
| 4.3.51 | 查询指定处理器资源信息 | 15 | `AggregateTotalCount`, `BandWidth`, `Bank`, `Boards`, `ErrorCount`, `Family`, `Metrics`, `NpuBoardSerialNumber`, `OtherParameters`, `PhysicalAddress`, `Ports`, `RowColumn`, `StackPcId`, `Time`, `TotalEnabledCores` |
| 4.2.17 | 修改PoDManager服务信息 | 15 | `AccessMode`, `CommunityString`, `CommunityStrings`, `EnableSNMPv1`, `EnableSNMPv2c`, `EnableSNMPv3`, `HideCommunityStrings`, `HttpProtocolVersion`, `NTPServers`, `NetworkSuppliedServers`, `Port1`, `Port2`, `RMCPEnabled`, `RMCPPlusEnabled`, `iBMCBMC服务资源信息` |
| 4.10.2.7 | 查询SSL证书更新服务资源信息 | 14 | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber`, `ServerCert`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo` |
| 4.10.2.8 | 修改SSL证书更新服务资源信息 | 14 | `CACertChainInfo`, `CrlValidFrom`, `CrlValidTo`, `FingerPrint`, `IsImportCrl`, `IssueBy`, `IssueTo`, `KeyUsage`, `PublicKeyLengthBits`, `SerialNumber`, `ServerCert`, `SignatureAlgorithm`, `ValidFrom`, `ValidTo` |
| 4.10.1.5 | 查询指定用户 | 14 | `@Redfish.ActionInfo`, `FingerPrint`, `HostBootstrapAccount`, `IssueBy`, `IssueTo`, `LastLoginIp`, `RevokedDate`, `RevokedState`, `RootCertUploadedState`, `SSHPublicKeyHash`, `SerialNumber`, `ValidFrom`, `ValidTo`, `target` |
| 4.6.3 | 查询指定任务资源信息 | 13 | `Description`, `EndTime`, `EstimatedDuration`, `Message`, `MessageArgs`, `MessageId`, `MessageSeverity`, `Messages`, `PercentComplete`, `RelatedProperties`, `Resolution`, `Severity`, `SubTasks` |
| 4.2.75 | 查询全量告警信息 | 12 | `Created`, `EntryType`, `EventId`, `EventSubject`, `EventType`, `HandlingSuggestion`, `Level`, `Message`, `MessageArgs`, `MessageId`, `Severity`, `SystemId` |
| 4.4.25 | 查询网络端口上接的光模块资源信息 | 12 | `@Redfish.ActionInfo`, `Actions`, `ContaminationDetection`, `LaneMappings`, `Location`, `LocationOrdinalValue`, `LocationType`, `PartLocation`, `PartLocationContext`, `RXFCSErrors`, `ServiceLabel`, `target` |
| 4.4.20 | 查询网络适配器单个资源信息 | 11 | `Actions`, `Assembly`, `Metrics`, `NetworkDeviceFunctions`, `Ports`, `PreloadPortCount`, `PreloadPortCountAllowableValues`, `Processors`, `RootBDFs`, `SerialNumber`, `target` |
| 4.10.7.1 | 导入CA证书 | 11 | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState`, `TaskStatus` |
| 4.4.3 | 修改指定机柜资源信息 | 11 | `BackupBatteryUnits`, `Board`, `Chassis`, `ChassisLocation`, `ManufacturingDate`, `MezzCardNum`, `Presence`, `ProductName`, `SDCardNum`, `SDContollerNum`, `Type` |
| 4.10.7.5 | 导入CA证书吊销列表 | 11 | `@odata.context`, `@odata.id`, `Description`, `Id`, `Messages`, `Name`, `PercentComplete`, `StartTime`, `TaskPercentage`, `TaskState`, `TaskStatus` |
| 4.2.5 | 修改SNMP资源属性 | 10 | `@Redfish.ActionInfo`, `Actions`, `BobEnabled`, `Links`, `LoginRule`, `PasswordPattern`, `PasswordRulePolicy`, `SNMP资源信息`, `TrapMode`, `target` |
| 4.2.28 | 查询Syslog资源信息 | 10 | `ReportType`, `RootCertificate.Issuer`, `RootCertificate.KeyUsage`, `RootCertificate.PublicKeyLengthBits`, `RootCertificate.SerialNumber`, `RootCertificate.SignatureAlgorithm`, `RootCertificate.Subject`, `RootCertificate.ValidNotAfter`, `RootCertificate.ValidNotBefore`, `Syslog资源信息` |
| 4.2.51 | 查询SP服务的诊断配置资源 | 10 | `ActionOnCompleted`, `AssetVerification`, `CountItem`, `CountValue`, `CountVerification`, `DumpEnabled`, `LogDump`, `PushTimeoutMinutes`, `RebootDelayMinutes`, `SP服务的诊断配置资源的信息` |
| 4.2.63 | 查询诊断服务资源 | 10 | `DeteriorationPredictionEnabled`, `DiagnosticService.ExportDiagnosticMetrics`, `DiagnosticService.StartCollectDrivesLog`, `DiskSubhealthFunction`, `DrivesLogCollectEnable`, `DrivesLogCollectInterval`, `LifespanEstimateAlarmEnabled`, `LifespanEstimateEnabled`, `OpticalModuleSubhealthFunction`, `PRBSTest` |
| 4.4.50 | 查询漏液检测 | 10 | `LeakDetectorType`, `Location`, `Manufacturer`, `Model`, `PartLocation`, `PartNumber`, `PhysicalContext`, `Reference`, `SerialNumber`, `ServiceLabel` |
| 4.6.6 | 查询指定子任务资源信息 | 10 | `Description`, `EndTime`, `EstimatedDuration`, `MessageArgs`, `MessageId`, `MessageSeverity`, `RelatedProperties`, `Resolution`, `Severity`, `StartTime` |
| 4.4.35 | 查询指定PCIe设备资源信息 | 9 | `DeviceType`, `HotPluggable`, `Lanes`, `MaxPCIeType`, `PCIeType`, `PowerState`, `Processors`, `ReadyToRemove`, `SlotType` |
| 4.4.9 | 查询指定机柜电源信息 | 9 | `BatteryMetricsExtended`, `BatteryPresenceState`, `EODAlarmState`, `PSUInputAStatus`, `PSUInputBStatus`, `RatedCapacityWattHour`, `RemainCapacityWattHour`, `VinChannelAVoltage`, `VinChannelBVoltage` |
| 4.4.14 | 查询指定机柜电源子系统信息 | 9 | `Allocation`, `CapacityWatts`, `MaxSupportedInGroup`, `MinNeededInGroup`, `PowerSupplies`, `PowerSupplyRedundancy`, `RedundancyGroup`, `RedundancyType`, `Status` |
| 4.2.109 | 查询FDMService服务资源 | 8 | `CPUFaultIsolationSubFunction`, `CacheWayFPCEnabled`, `CoreIsolationAlarmThreshold`, `CpuFPC`, `FDMService资源的信息`, `MemRowSparingEnabled`, `MemoryDynamicRemappingEnabled`, `NpuFPC` |
| 4.3.18 | 查询指定主机以太网接口资源信息 | 8 | `EthernetInterfaceType`, `Links`, `MTUSize`, `Ports`, `VLAN`, `VLANEnable`, `VLANId`, `VLANPriority` |
| 4.4.27 | 查询指定驱动器资源信息 | 8 | `Assembly`, `DriveFormFactor`, `FormFactor`, `LocationIndicatorActive`, `Metrics`, `PartNumber`, `PhysicalLocation`, `SlotPowerState` |
| 4.4.45 | 查询指定机柜泵资源信息 | 8 | `CoolantConnectorRedundancy`, `FanRedundancy`, `FanSpeedDeviationThresholdPercent`, `MaxSupportedInGroup`, `MinNeededInGroup`, `RedundancyGroup`, `RedundancyType`, `ThermalMetrics` |
| 4.6.4 | 查询指定任务运行信息 | 7 | `@odata.type`, `Message`, `MessageArgs`, `MessageId`, `RelatedProperties`, `Resolution`, `Severity` |
| 4.1.3 | 修改当前根服务资源 | 6 | `Fabrics`, `JobService`, `KerberosEnabled`, `ObservabilityService`, `Product`, `Vendor` |
| 4.2.2 | 查询指定管理资源信息 | 6 | `Manager.QuickDump`, `Manager.ResetToDefaults`, `Scope`, `ShelfPowerButtonMode`, `VenderName`, `WirelessService` |
| 4.2.40 | 查询SP服务的OS安装配置资源 | 6 | `FirstBootScriptFile`, `IPv4RouteSettings`, `IPv6RouteSettings`, `Metric`, `OS安装配置资源信息`, `TableId` |
| 4.2.110 | 修改FDMService服务资源属性 | 6 | `CPUFaultIsolationSubFunction`, `CacheWayFPCEnabled`, `CoreIsolationAlarmThreshold`, `FDMService资源的信息`, `MemRowSparingEnabled`, `MemoryDynamicRemappingEnabled` |
| 4.4.28 | 修改指定驱动器属性 | 6 | `Assembly`, `DriveFormFactor`, `LocationIndicatorActive`, `Metrics`, `PartNumber`, `PhysicalLocation` |
| 4.4.52 | 查询风扇单个资源信息 | 6 | `DataSourceUri`, `Location`, `LocationOrdinalValue`, `LocationType`, `PartLocation`, `ServiceLabel` |
| 4.2.9 | 查询NTP资源 | 6 | `Actions`, `CurrentPollingIntervalSeconds`, `Id`, `NTPKeyStatus`, `NTP配置资源信息`, `Name` |
| 4.10.4.3 | 查询指定会话 | 6 | `AccountInsecurePromptEnabled`, `ClientOriginIPAddress`, `CreatedTime`, `OemSessionType`, `Roles`, `SessionType` |
| 4.3.16 | 查询虚拟SP U盘资源 | 5 | `ConnectedVia`, `Image`, `ImageName`, `Inserted`, `MediaTypes` |
| 4.2.39 | 创建SP服务的OS安装配置 | 5 | `FirstBootScriptFile`, `IPv4RouteSettings`, `IPv6RouteSettings`, `Metric`, `TableId` |
| 4.2.13 | 修改LLDP服务资源信息 | 5 | `LLDP服务资源信息`, `TxDelaySeconds`, `TxHold`, `TxIntervalSeconds`, `WorkMode` |
| 4.3.26 | 查询指定内存资源信息 | 5 | `BomNumber`, `ControllerTemperatureCelsius`, `EccCount`, `MediumTemperatureCelsius`, `RemainingServiceLifePercent` |
| 4.7.1 | 查询事件服务资源 | 5 | `DeliveryRetryAttempts`, `DeliveryRetryIntervalSeconds`, `EventService资源信息`, `SnmpReportType`, `Status` |
| 4.7.2 | 修改事件服务资源 | 5 | `DeliveryRetryAttempts`, `DeliveryRetryIntervalSeconds`, `EventService资源信息`, `SnmpReportType`, `Status` |
| 4.8.1 | 查询数据采集服务资源 | 5 | `DataAcquisitionService资源信息`, `DataSource@Redfish.AllowableValues`, `HwDataAcquisitionService.ClearHistoryData`, `HwDataAcquisitionService.DataFiltering`, `HwDataAcquisitionService.ExportAcquisitionData` |
| 4.2.10 | 修改NTP资源 | 5 | `Actions`, `Id`, `NTPKeyStatus`, `NTP资源信息`, `Name` |
| 4.10.4.2 | 创建会话（登录） | 5 | `ClientOriginIPAddress`, `CreatedTime`, `OemSessionType`, `Roles`, `SessionType` |
| 4.1.8 | 查询所有归档资源 | 4 | `Base.v1_0_0`, `BiosAttributeRegistry.v1_0_1`, `iBMC.v1_0_0`, `iBMCEvents.v2_0_10` |
| 4.10.8.2 | 更新系统主密钥 | 4 | `@odata.context`, `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.50 | 创建SP服务的诊断配置 | 4 | `AssetVerification`, `CountItem`, `CountValue`, `CountVerification` |
| 4.3.3 | 修改指定系统资源属性 | 4 | `DelaySecondsAfterCpuThermalTrip`, `PowerMode`, `PowerOnAfterCpuThermalTrip`, `SSDMediaLifeLeftPercentThreshold` |
| 4.3.60 | 批量查询处理器资源信息 | 4 | `EccInfo`, `MultiBitIsolatedPages`, `OperatingSpeedMHz`, `SingleBitIsolatedPages` |
| 4.4.40 | 查询指定PCIe功能资源信息 | 4 | `ClassCode`, `FunctionProtocol`, `FunctionType`, `SegmentNumber` |
| 4.4.48 | 查询漏液检测系统信息 | 4 | `Health`, `HealthRollup`, `State`, `Status` |
| 4.5.5 | 生效固件 | 4 | `Description`, `Messages`, `PercentComplete`, `TaskStatus` |
| 4.8.2 | 修改数据采集服务开关状态 | 4 | `DataSource@Redfish.AllowableValues`, `HwDataAcquisitionService.ClearHistoryData`, `HwDataAcquisitionService.DataFiltering`, `HwDataAcquisitionService.ExportAcquisitionData` |
| 4.3.14 | 连接虚拟媒体 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.15 | 断开虚拟媒体 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.7 | 修改VNC资源属性 | 3 | `DisableKeyboardDuringBiosStartup`, `PasswordPattern`, `PasswordRulePolicy` |
| 4.2.86 | 更新SP相关的schema文件 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.87 | 收集SP相关的日志信息 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.59 | 安装SP插件 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.69 | 导出录像 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.72 | 导出黑匣子 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.73 | 导出串口数据 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.25 | 导出日志信息 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.94 | 内存隔离联动模式下发隔离任务 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.2.113 | 查询场景化智能节能信息 | 3 | `EnergySavingStatus`, `EnergySavingStatusPerDomain`, `NPUSubsystem` |
| 4.3.19 | 配置以太网 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.22 | 配置Bond | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.30 | 配置VLAN | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.32 | 查询指定存储资源信息 | 3 | `EpdSupported`, `JbodStateSupported`, `PhyId` |
| 4.3.39 | 删除指定逻辑盘 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.40 | 创建逻辑盘 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.3.13 | 设置虚拟媒体资源 | 3 | `EjectPolicy`, `EjectTimeout`, `Password` |
| 4.4.13 | 收集功率统计数据 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.4.39 | 指定PCIe设备资源导入https证书 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.8.3 | 清空“数据采集点信息表” | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.9.1 | 查询遥测服务资源信息 | 3 | `TelemetryService.ResetMetricReportDefinitionsToDefaults`, `TelemetryService.ResetTriggersToDefaults`, `TelemetryService.SubmitTestMetricReport` |
| 4.9.2 | 修改遥测服务资源信息 | 3 | `TelemetryService.ResetMetricReportDefinitionsToDefaults`, `TelemetryService.ResetTriggersToDefaults`, `TelemetryService.SubmitTestMetricReport` |
| 4.2.70 | 截图 | 3 | `Description`, `PercentComplete`, `TaskStatus` |
| 4.10.2.3 | 查询会话策略 | 3 | `SessionService资源信息`, `WebSessionMode`, `WebSessionTimeoutMinutes` |
| 4.10.2.4 | 修改会话策略 | 3 | `SessionService资源信息`, `WebSessionMode`, `WebSessionTimeoutMinutes` |
| 4.4.49 | 查询漏液检测器集合 | 2 | `Members`, `Members@odata.count` |
| 4.7.10 | 删除事件订阅资源 | 2 | `@Message.ExtendedInfo`, `RelatedProperties` |
| 4.7.11 | 屏蔽系统事件上报 | 2 | `@Message.ExtendedInfo`, `RelatedProperties` |
| 4.10.2.5 | 查询证书策略 | 2 | `CRLEnabled`, `CertificateService资源信息` |
| 4.10.2.6 | 修改证书策略 | 2 | `CRLEnabled`, `CertificateService资源信息` |
| 4.2.7 | SNMP发送测试事件 | 1 | `SNMP发送测试事件信息` |
| 4.3.8 | 查询KVM资源 | 1 | `DisableKeyboardDuringBiosStartup` |
| 4.3.9 | 修改KVM资源属性 | 1 | `DisableKeyboardDuringBiosStartup` |
| 4.2.21 | 查询安全服务集合资源信息 | 1 | `ComponentMeasurementPolicy` |
| 4.2.22 | 修改安全服务集合资源信息 | 1 | `ComponentMeasurementPolicy` |
| 4.2.38 | 查询SP服务的OS安装配置集合资源 | 1 | `OS安装配置集合资源信息` |
| 4.2.54 | 查询SP服务的硬盘擦除配置资源 | 1 | `SP服务的硬盘擦除配置资源的信息` |
| 4.2.55 | 查询SP系统擦除配置集合资源 | 1 | `SP系统擦除配置集合配置资源的信息` |
| 4.2.56 | 创建SP系统擦除配置 | 1 | `SP系统擦除配置的信息` |
| 4.2.57 | 查询指定SP系统擦除配置 | 1 | `SP系统擦除配置的信息` |
| 4.2.60 | 查询SP插件集合资源 | 1 | `SP插件集合资源信息` |
| 4.2.61 | 查询SP插件资源 | 1 | `SP插件资源信息` |
| 4.2.26 | 查询日志集合资源信息 | 1 | `Members@odata.nextLink` |
| 4.2.12 | 查询LLDP服务资源信息 | 1 | `LLDP服务配置资源信息` |
| 4.2.111 | 查询USB管理服务资源信息 | 1 | `USB管理服务配置资源信息` |
| 4.2.112 | 修改USB管理服务资源信息 | 1 | `USB管理服务配置资源信息` |
| 4.2.92 | 查询FPCService服务资源 | 1 | `FPCService资源的信息` |
| 4.2.115 | 查询TPCM服务信息 | 1 | `Tpcm服务配置资源信息` |
| 4.2.116 | 设置TPCM服务信息 | 1 | `Tpcm服务配置资源信息` |
| 4.3.5 | FRU上下电控制 | 1 | `FRU上下电控制信息` |
| 4.3.20 | 查询Bond集合资源信息 | 1 | `Bond集合资源信息` |
| 4.3.21 | 查询Bond资源信息 | 1 | `Bond资源信息` |
| 4.3.28 | 查询VLAN集合资源信息 | 1 | `VLAN集合资源信息` |
| 4.3.29 | 查询VLAN资源信息 | 1 | `VLAN资源信息` |
| 4.3.33 | 修改指定控制器资源信息 | 1 | `PhyId` |
| 4.3.45 | 修改BIOS设置资源属性 | 1 | `BIOS设置资源信息` |
| 4.3.47 | 查询BIOS策略重配资源信息 | 1 | `BIOS策略重配属性列表` |
| 4.3.49 | 修改BIOS策略重配设置资源属性 | 1 | `BIOS策略重配设置资源信息` |
| 4.3.56 | 查询CPU历史占用率资源信息 | 1 | `CPU历史占用率资源信息` |
| 4.3.63 | 查询IB集合资源信息 | 1 | `IB集合资源信息` |
| 4.3.64 | 查询IB资源信息 | 1 | `IB资源信息` |
| 4.4.22 | 查询网络端口单个资源信息 | 1 | `PortState` |
| 4.4.23 | 修改网络端口单个资源信息 | 1 | `LldpEnabled` |
| 4.4.33 | NPU模组复位 | 1 | `NPU模组复位信息` |
| 4.4.34 | 查询PCIe设备集合资源信息 | 1 | `PCIe设备集合资源信息` |
| 4.4.36 | 修改指定PCIe设备资源信息 | 1 | `ReadyToRemove` |
| 4.4.56 | 查询Sensors集合资源 | 1 | `Sensors资源信息` |
| 4.4.57 | 查询指定Sensor资源信息 | 1 | `sensor资源信息` |
| 4.10.1.3 | 删除用户 | 1 | `code` |
| 4.10.3.2 | 查询指定角色信息 | 1 | `RoleId` |
| 4.10.9.1 | 查询Ldap服务资源 | 1 | `Ldap服务资源信息` |
| 4.10.9.2 | 修改Ldap功能开启使能 | 1 | `Ldap服务资源信息` |
| 4.10.9.3 | 查询Ldap域控制器集合信息 | 1 | `Ldap域控制器集合` |
| 4.10.9.5 | 修改具体域控制器的信息 | 1 | `GroupDomain` |
| 4.5.3 | 查询指定可升级固件资源信息 | 1 | `Staged` |
| 4.6.1 | 查询任务服务资源信息 | 1 | `TaskAutoDeleteTimeoutMinutes` |
| 4.7.6 | 查询事件订阅集合资源 | 1 | `EventService资源信息` |
| 4.8.5 | 查询数据表资源信息 | 1 | `IndicatorLED` |
| 4.10.7.2 | 删除CA证书 | 1 | `CA证书删除信息` |
| 4.12.1 | 查询资源服务信息 | 1 | `AssetService资源信息` |
| 4.12.2 | 查询硬件资产清单信息 | 1 | `AssetList资源信息` |
| 4.9.11 | 查询指定指标报告资源信息 | 1 | `Timestamp` |
| 4.9.17 | 提交测试指标报告上报 | 1 | `SubmitTestMetricReport资源信息` |
| 4.2.11 | 导入NTP密钥 | 1 | `NTP服务器密钥导入信息` |
| 4.2.29 | 修改Syslog资源信息 | 1 | `ReportType` |
| 4.2.18 | 查询PoDManager网卡集合信息 | 1 | `iBMCBMC网口集合资源信息` |
| 4.4.46 | 修改指定机柜泵资源信息 | 1 | `FanSpeedDeviationThresholdPercent` |
| 4.5.4 | 批量升级固件 | 1 | `Description` |
| 4.9.18 | 清除指标报告（未开发） | 1 | `SubmitTestMetricReport资源信息` |
| 4.9.19 | 恢复指标报告定义到默认值 （未开发） | 1 | `SubmitTestMetricReport资源信息` |
| 4.9.20 | 恢复触发器到默认值 (未开发) | 1 | `SubmitTestMetricReport资源信息` |

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

