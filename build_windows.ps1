# Build on Windows (PowerShell). No install or network required after packaging.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Set-Location $PSScriptRoot

$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { 'py' }
& $python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Error al instalar dependencias' }
& $python -m pip install 'pyinstaller>=6,<7'
if ($LASTEXITCODE -ne 0) { throw 'Error al instalar PyInstaller' }

& $python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Pruebas fallidas: se cancela el empaquetado' }

& $python -m PyInstaller --noconfirm --clean --onedir --windowed --name MaizUrbano --add-data 'frontend;frontend' main.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller no pudo compilar' }

$dest = Join-Path $PSScriptRoot 'dist\MaizUrbano'
$exe = Join-Path $dest 'MaizUrbano.exe'
$ui = Join-Path $dest '_internal\frontend\index.html'
if (-not (Test-Path $exe -PathType Leaf)) { throw "Falta el ejecutable: $exe" }
if (-not (Test-Path $ui -PathType Leaf)) { throw "Faltan los recursos HTML: $ui" }

New-Item -ItemType Directory -Force -Path (Join-Path $dest 'data') | Out-Null
# Runs the packaged executable without a GUI. Validates the bundled HTML/CSS/JS
# and writes/reopens a TEMPORARY SQLite DB under data/, then removes it.
$process = Start-Process -FilePath $exe -ArgumentList '--self-check' -PassThru -Wait
if ($process.ExitCode -ne 0) { throw "La prueba del ejecutable fallo: $($process.ExitCode)" }

Write-Host 'Listo: dist\MaizUrbano\MaizUrbano.exe' -ForegroundColor Green
Write-Host 'Datos persistentes: dist\MaizUrbano\data\maiz_urbano.db' -ForegroundColor Yellow
Write-Host 'Conserva la carpeta completa. Falta la validacion visual con WebView2 en Windows.' -ForegroundColor Yellow
