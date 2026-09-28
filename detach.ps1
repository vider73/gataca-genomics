<#
Run a long GATACA job outside any Claude session, as a one-off Windows scheduled task.

  .\detach.ps1 -Name emo_queue -Command "bash runs/2026-09-28/queue_emotion.sh"
  .\detach.ps1 -List
  .\detach.ps1 -Stop -Name emo_queue

Background jobs started from a Claude session die when the session restarts. A scheduled task does not:
Windows runs it, it survives session restarts, and it unregisters itself when the job ends.
- The command runs in Git Bash from the project folder, with the Python found at launch time first on
  PATH (the scheduled task does not inherit the session's environment).
- The command is saved as runs/jobs/<name>.sh; its output goes to runs/jobs/<name>.log.
- -Stop ends the task and kills the job's process tree (use it instead of killing processes by hand).
#>
param([string]$Name, [string]$Command, [switch]$Run, [switch]$List, [switch]$Stop)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$jobs = Join-Path $root "runs\jobs"
New-Item -ItemType Directory $jobs -Force | Out-Null
$bash = "C:\Program Files\Git\bin\bash.exe"
function TaskName($n) { "GATACA job $n" }
function Stamp { Get-Date -Format "yyyy-MM-ddTHH:mm:ss" }
function ToPosix($p) { "/" + $p.Substring(0, 1).ToLower() + ($p.Substring(2) -replace "\\", "/") }

if ($List) {
  Get-ScheduledTask -TaskName "GATACA job *" -ErrorAction SilentlyContinue |
    Select-Object @{n = "job"; e = { $_.TaskName -replace "^GATACA job ", "" } }, State | Format-Table
  return
}
if (-not $Name) { throw "-Name is required" }
$script = Join-Path $jobs "$Name.sh"
$log = Join-Path $jobs "$Name.log"
$pidFile = Join-Path $jobs "$Name.pid"

if ($Stop) {
  if (Test-Path $pidFile) {
    & taskkill /PID (Get-Content $pidFile) /T /F | Out-Null
    Remove-Item $pidFile
  }
  Stop-ScheduledTask -TaskName (TaskName $Name) -ErrorAction SilentlyContinue
  Unregister-ScheduledTask -TaskName (TaskName $Name) -Confirm:$false -ErrorAction SilentlyContinue
  Add-Content $log "[$(Stamp)] stopped by hand"
  "stopped job $Name"
  return
}

if ($Run) {
  # Inside the scheduled task: run the job, then remove the task.
  Add-Content $log "[$(Stamp)] start"
  $p = Start-Process -FilePath $bash -ArgumentList "`"$script`"" -WorkingDirectory $root -NoNewWindow -PassThru `
    -RedirectStandardOutput "$log.out" -RedirectStandardError "$log.err"
  Set-Content $pidFile $p.Id
  $p.WaitForExit()
  Get-Content "$log.out", "$log.err" -ErrorAction SilentlyContinue | Add-Content $log
  Remove-Item "$log.out", "$log.err", $pidFile -ErrorAction SilentlyContinue
  Add-Content $log "[$(Stamp)] exit $($p.ExitCode)"
  Unregister-ScheduledTask -TaskName (TaskName $Name) -Confirm:$false -ErrorAction SilentlyContinue
  return
}

# Register and start.
if (-not $Command) { throw "-Command is required" }
if (Get-ScheduledTask -TaskName (TaskName $Name) -ErrorAction SilentlyContinue) { throw "job '$Name' already exists" }
$pyDir = ToPosix (Split-Path (Get-Command python).Source)
Set-Content -Path $script -Encoding utf8NoBOM -Value @"
#!/bin/bash
export PATH="$pyDir`:`$PATH"
export PYTHONUNBUFFERED=1
cd "$(ToPosix $root)"
$Command
"@
$action = New-ScheduledTaskAction -Execute "pwsh.exe" -WorkingDirectory $root `
  -Argument "-NoProfile -WindowStyle Hidden -File `"$root\detach.ps1`" -Name $Name -Run"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(5)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
  -ExecutionTimeLimit (New-TimeSpan -Days 3)
Register-ScheduledTask -TaskName (TaskName $Name) -Description "GATACA detached job: $Command" `
  -Action $action -Trigger $trigger -Settings $settings | Out-Null
"launched job '$Name' -> log runs/jobs/$Name.log"
