# Check today's activity including hibernate/resume
$today = (Get-Date).Date
Write-Host "Checking today's PC activity (hibernate/resume/logon)..." -ForegroundColor Green
Write-Host "Today: $($today.ToString('yyyy-MM-dd'))" -ForegroundColor Yellow
Write-Host ""

# Event IDs to check:
# 1 - System time changed (often around resume)
# 42 - System resumed from hibernate/sleep
# 6005 - System startup (in case of full boot)
# 6006 - System shutdown
# 4624 - Logon events (in Security log)

$events = Get-WinEvent -LogName System -ErrorAction SilentlyContinue | Where-Object {
    $_.TimeCreated -ge $today -and $_.Id -in @(1, 42, 6005, 6006)
}

if ($events) {
    Write-Host "Today's system events:" -ForegroundColor Green
    $events | Sort-Object TimeCreated | ForEach-Object {
        $eventType = switch ($_.Id) {
            1 { "TIME_CHANGE" }
            42 { "RESUME_FROM_HIBERNATE" }
            6005 { "SYSTEM_STARTUP" }
            6006 { "SYSTEM_SHUTDOWN" }
            default { "OTHER" }
        }
        
        $color = switch ($_.Id) {
            42 { "Cyan" }
            6005 { "Green" }
            6006 { "Red" }
            default { "White" }
        }
        
        Write-Host "$($_.TimeCreated.ToString('HH:mm:ss')) - $eventType" -ForegroundColor $color
    }
} else {
    Write-Host "No system events found for today" -ForegroundColor Yellow
}

Write-Host "`nChecking logon events..." -ForegroundColor Green
$logonEvents = Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624; StartTime=$today} -ErrorAction SilentlyContinue
if ($logonEvents) {
    Write-Host "Today's logons:" -ForegroundColor Green
    $logonEvents | Sort-Object TimeCreated | ForEach-Object {
        $user = $_.Properties[5].Value
        Write-Host "$($_.TimeCreated.ToString('HH:mm:ss')) - Logon by: $user" -ForegroundColor Cyan
    }
} else {
    Write-Host "No logon events found for today" -ForegroundColor Yellow
}

# Check for power state changes (hibernate/sleep)
Write-Host "`nChecking power events..." -ForegroundColor Green
$powerEvents = Get-WinEvent -LogName System -ErrorAction SilentlyContinue | Where-Object {
    $_.TimeCreated -ge $today -and (
        $_.Message -like "*hibernate*" -or 
        $_.Message -like "*sleep*" -or 
        $_.Message -like "*resume*" -or
        $_.Id -eq 42
    )
}

if ($powerEvents) {
    Write-Host "Power state changes today:" -ForegroundColor Green
    $powerEvents | Sort-Object TimeCreated | ForEach-Object {
        $shortMessage = if ($_.Message.Length -gt 80) { $_.Message.Substring(0, 80) + "..." } else { $_.Message }
        Write-Host "$($_.TimeCreated.ToString('HH:mm:ss')) - ID $($_.Id): $shortMessage" -ForegroundColor Yellow
    }
} else {
    Write-Host "No power state changes found for today" -ForegroundColor Yellow
}

# Check current session info
Write-Host "`nCurrent session info:" -ForegroundColor Green
$lastBoot = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
$uptime = (Get-Date) - $lastBoot
Write-Host "Last full boot: $lastBoot" -ForegroundColor Yellow
Write-Host "Uptime: $([math]::Round($uptime.TotalHours, 2)) hours" -ForegroundColor Yellow

if ($lastBoot.Date -eq $today) {
    Write-Host "PC was booted TODAY" -ForegroundColor Green
} else {
    Write-Host "PC was last booted: $($lastBoot.ToString('yyyy-MM-dd'))" -ForegroundColor Yellow
}