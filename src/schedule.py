import json
from datetime import datetime

# Load times from a JSON file
with open('./../data/schedule.json', 'r') as file:
    data = json.load(file)

# Function to calculate total active time for a specific day
def calculate_total_active_time(day):
    total_active_minutes = 0
    for session in day['sessions']:
        start_time = datetime.strptime(f"{day['date']} {session['start']}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{day['date']} {session['end']}", "%Y-%m-%d %H:%M")
        duration = (end_time - start_time).total_seconds() / 60  # duration in minutes
        total_active_minutes += duration
    
    return total_active_minutes

# Initialize total active time for the month
monthly_active_minutes = 0

# Iterate through the days and calculate total active time for each
for day in data['days']:
    total_active_minutes = calculate_total_active_time(day)
    monthly_active_minutes += total_active_minutes  # Accumulate for the month

    total_active_hours = total_active_minutes // 60
    remaining_minutes = total_active_minutes % 60
    day['total_active_time'] = {
        "hours": int(total_active_hours),
        "minutes": int(remaining_minutes)
    }

# Calculate total active time for the month
monthly_active_hours = monthly_active_minutes // 60
monthly_remaining_minutes = monthly_active_minutes % 60

# Add monthly total to the data
data['monthly_total_active_time'] = {
    "hours": int(monthly_active_hours),
    "minutes": int(monthly_remaining_minutes)
}

# Write the updated data back to the JSON file with 2 spaces indentation
with open('./../data/schedule.json', 'w') as file:
    json.dump(data, file, indent=2)

# Print confirmation message
print("Total active times calculated and written to schedule.json")
