# 一键启动 Portfolio 内容管理后台
# 后端 8002 + 前端 5175（隐藏窗口后台运行）
$root = $PSScriptRoot
$server = Join-Path $root "server"
$web = Join-Path $root "web"

# 后端（首次自动建 venv 并安装依赖）
Start-Process powershell -WindowStyle Hidden -ArgumentList @(
  "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $server "run.ps1")
)

# 前端
Start-Process powershell -WindowStyle Hidden -ArgumentList @(
  "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
  "Set-Location -LiteralPath '$web'; npm run dev"
)

Start-Sleep -Seconds 2
Write-Output "管理界面: http://localhost:5175"
Write-Output "后端接口: http://localhost:8002/docs"
