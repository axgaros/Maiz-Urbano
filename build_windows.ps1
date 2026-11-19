# Ejecutar en PowerShell desde la carpeta del proyecto, con Python instalado.
$ErrorActionPreference = 'Stop'
py -m pip install -r requirements.txt
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --onedir --windowed --name MaizUrbano --add-data 'frontend;frontend' main.py
Write-Host 'Carpeta generada: dist\MaizUrbano\' -ForegroundColor Yellow
Write-Host 'Abre MaizUrbano.exe. La base de datos se creara en dist\MaizUrbano\data\' -ForegroundColor Yellow