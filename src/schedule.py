import json
from datetime import datetime

# Load times from a JSON file
with open('./../data/schedule.json', 'r') as file:
    data = json.load(file)

# Extract active times for the specified day
active_times_extended = []
date_to_check = "2024-10-09"

for day in data['days']:
    if day['date'] == date_to_check:
        active_times_extended = [
            (f"{date_to_check} {session['start']}", f"{date_to_check} {session['end']}")
            for session in day['sessions']
        ]

# Calculate total active duration for the extended list
total_active_minutes_extended = 0

for start, end in active_times_extended:
    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
    duration = (end_time - start_time).total_seconds() / 60  # duration in minutes
    total_active_minutes_extended += duration

# Convert total active minutes to hours and minutes
total_active_hours_extended = total_active_minutes_extended // 60
remaining_minutes_extended = total_active_minutes_extended % 60

# Print the total active time
print(f"Total active time for {date_to_check}: {int(total_active_hours_extended)} hours and {int(remaining_minutes_extended)} minutes")
