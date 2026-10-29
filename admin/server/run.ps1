# 启动内容管理后台后端（FastAPI）
# 默认端口 8002，口令见环境变量 ADMIN_TOKEN（默认 admin123）
param(
    [int]$Port = 8002
)
$root = Split-Path -Parent $PSScriptRoot
$venv = Join-Path $root ".venv"

# 首次运行：创建虚拟环境并安装依赖
if (-not (Test-Path -LiteralPath (Join-Path $venv "Scripts\python.exe"))) {
    python -m venv $venv
    & (Join-Path $venv "Scripts\python.exe") -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
}

& (Join-Path $venv "Scripts\python.exe") -m uvicorn app.main:app --reload --port $Port --app-dir $PSScriptRoot
