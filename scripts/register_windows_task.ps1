# Nexus 24/7 Autonomous Revenue Task Registration Script
# Registers a Windows Scheduled Task to execute the Revenue Daemon continuously
# -----------------------------------------------------------------------------

$TaskName = "Nexus-24x7-RevenueDaemon"
$PythonPath = (Get-Command python).Source
$ScriptDir = Split-Path -Parent $PSScriptRoot
$ScriptPath = Join-Path $ScriptDir "scripts\revenue_daemon.py"

Write-Host "Registering Windows Scheduled Task: $TaskName" -ForegroundColor Cyan
Write-Host "Python Path: $PythonPath" -ForegroundColor Gray
Write-Host "Script Path: $ScriptPath" -ForegroundColor Gray

# Define action to run python scripts/revenue_daemon.py
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$ScriptPath`"" -WorkingDirectory $ScriptDir

# Define triggers: At system startup / login + Repeat every 1 hour indefinitely
$Trigger1 = New-ScheduledTaskTrigger -AtLogOn
$Trigger2 = New-ScheduledTaskTrigger -Daily -At "00:01AM"

$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)

try {
    # Attempt user-level task registration
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($Trigger1, $Trigger2) -Settings $Settings -User $env:USERNAME -Description "Nexus Autonomous Daily Revenue Negotiation & Base L2 Settlement Daemon" -ErrorAction Stop
    Write-Host "✅ Scheduled Task '$TaskName' registered successfully!" -ForegroundColor Green
    Write-Host "Run now with: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Yellow
} catch {
    Write-Warning "ScheduledTask requires admin elevation: $_"
    Write-Host "Creating seamless Windows User Startup entry instead (No admin required)..." -ForegroundColor Yellow

    $StartupFolder = [Environment]::GetFolderPath('Startup')
    $ShortcutPath = Join-Path $StartupFolder "Nexus-RevenueDaemon.lnk"

    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $PythonPath
    $Shortcut.Arguments = "`"$ScriptPath`" --loop"
    $Shortcut.WorkingDirectory = $ScriptDir
    $Shortcut.WindowStyle = 7 # Minimized
    $Shortcut.Description = "Nexus 24/7 Autonomous Daily Revenue Daemon"
    $Shortcut.Save()

    Write-Host "✅ Successfully installed auto-start shortcut into Windows Startup folder:" -ForegroundColor Green
    Write-Host "   $ShortcutPath" -ForegroundColor Cyan
    Write-Host "   The Revenue Daemon will now launch automatically in background on every Windows login!" -ForegroundColor Green
}
