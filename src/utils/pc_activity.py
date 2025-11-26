import subprocess
import json
from datetime import datetime, timedelta

def run_powershell(command):
    """Run PowerShell command and return output"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def get_today_activity():
    """Get today's PC activity times"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    print("=== Today's PC Activity ===")
    print(f"Date: {today.strftime('%Y-%m-%d')}")
    print(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Get today's activity events (Event ID 1)
    print("Today's Activity Times:")
    ps_command = """
    $today = (Get-Date).Date
    $events = Get-WinEvent -LogName System -ErrorAction SilentlyContinue | Where-Object {
        $_.TimeCreated -ge $today -and $_.Id -eq 1
    }
    if ($events) {
        $events | Sort-Object TimeCreated | Select-Object TimeCreated -Unique | ForEach-Object {
            $_.TimeCreated.ToString('HH:mm:ss')
        }
    } else {
        "No activity found today"
    }
    """
    
    activity_output = run_powershell(ps_command)
    if activity_output and "Error" not in activity_output:
        times = [line.strip() for line in activity_output.split('\n') if line.strip()]
        if times and times[0] != "No activity found today":
            for time in times:
                print(f"  {time}")
            
            first_time = times[0]
            last_time = times[-1]
            print(f"\nFirst activity today: {first_time}")
            print(f"Last activity today:  {last_time}")
        else:
            print("  No activity found today")
    else:
        print("  Error retrieving activity data")
    
    # Get system information
    print("\nSystem Information:")
    ps_command = """
    $lastBoot = (Get-CimInstance -ClassName Win32_OperatingSystem).LastBootUpTime
    $uptime = (Get-Date) - $lastBoot
    Write-Output "Last boot: $($lastBoot.ToString('yyyy-MM-dd HH:mm:ss'))"
    Write-Output "Uptime: $([math]::Round($uptime.TotalHours, 2)) hours"
    """
    
    system_info = run_powershell(ps_command)
    if system_info and "Error" not in system_info:
        for line in system_info.split('\n'):
            print(f"  {line}")
    else:
        print("  Error retrieving system info")

def get_simple_activity():
    """Simple version - just get activity times"""
    print("Today's PC Wake Times:")
    print("-" * 25)
    
    ps_command = """
    $today = (Get-Date).Date
    Get-WinEvent -LogName System | Where-Object { 
        $_.TimeCreated -ge $today -and $_.Id -eq 1 
    } | Sort-Object TimeCreated | Select-Object TimeCreated -Unique | ForEach-Object {
        "Woke at: " + $_.TimeCreated.ToString('HH:mm:ss')
    }
    """
    
    output = run_powershell(ps_command)
    if output and "Error" not in output:
        lines = [line for line in output.split('\n') if line.strip()]
        if lines:
            for line in lines:
                print(line)
        else:
            print("No activity found today")
    else:
        print("Error retrieving data")

if __name__ == "__main__":
    # Run the detailed version
    get_today_activity()
    
    print("\n" + "="*50)
    
    # Run the simple version too
    get_simple_activity()