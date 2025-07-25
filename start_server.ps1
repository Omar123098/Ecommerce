# Django Server Starter for PowerShell
Write-Host "Starting Django server..." -ForegroundColor Green
Set-Location "d:\commerce\commerce"
& "D:\commerce\.venv\Scripts\python.exe" manage.py runserver
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
