param(
    [string]$Date = "20260507"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = (Resolve-Path (Join-Path $ScriptDir "..")).Path

function Get-EnvOrDefault {
    param(
        [string]$Name,
        [string]$Default
    )

    $Value = [Environment]::GetEnvironmentVariable($Name)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $Default
    }
    return $Value
}

function Resolve-PythonCommand {
    $ConfiguredPython = [Environment]::GetEnvironmentVariable("PYTHON")
    if (-not [string]::IsNullOrWhiteSpace($ConfiguredPython)) {
        return @($ConfiguredPython)
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @("py", "-3")
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @("python")
    }
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        return @("python3")
    }

    throw "missing Python command: install Python 3 or set the PYTHON environment variable"
}

$PodmDoc = Get-EnvOrDefault `
    -Name "PODM_DOC" `
    -Default (Join-Path $RootDir "data\$Date\Atlas PoDManager 1.0.0 Redfish 接口参考.docx")
$BmcDoc = Get-EnvOrDefault `
    -Name "BMC_DOC" `
    -Default (Join-Path $RootDir "data\$Date\华为服务器 iBMC300 Redfish 接口说明.docx")
$MatchWorkbook = Get-EnvOrDefault `
    -Name "MATCH_WORKBOOK" `
    -Default (Join-Path $RootDir "output\$Date\analysis\interface_match_llm_summary.xlsx")
$OutDir = Get-EnvOrDefault `
    -Name "OUT_DIR" `
    -Default (Join-Path $RootDir "output\$Date")

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

foreach ($Required in @($PodmDoc, $BmcDoc, $MatchWorkbook)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "missing required file: $Required"
    }
}

$PythonCommand = Resolve-PythonCommand
$PythonExe = $PythonCommand[0]
$PythonArgs = @()
if ($PythonCommand.Count -gt 1) {
    $PythonArgs = $PythonCommand[1..($PythonCommand.Count - 1)]
}

& $PythonExe @PythonArgs `
    (Join-Path $ScriptDir "extract_word_interface_params.py") `
    --profile bmc `
    --match-workbook $MatchWorkbook `
    --match-side bmc `
    $BmcDoc `
    -o (Join-Path $OutDir "bmc.common.word.interface-params.yaml")

& $PythonExe @PythonArgs `
    (Join-Path $ScriptDir "extract_word_interface_params.py") `
    --profile podm `
    --match-workbook $MatchWorkbook `
    --match-side podm `
    $PodmDoc `
    -o (Join-Path $OutDir "podm.common.word.interface-params.yaml")
