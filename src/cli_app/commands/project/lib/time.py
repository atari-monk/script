import json
from datetime import datetime
import os

# List of JSON file paths for different projects
project_files = [
    '../../data/morpheus_time_logger.json',
]

# Function to calculate total active time for a specific day
def calculate_total_active_time(day):
    total_active_minutes = 0
    for session in day['sessions']:
        start_time = datetime.strptime(f"{day['date']} {session['start']}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{day['date']} {session['end']}", "%Y-%m-%d %H:%M")
        duration = (end_time - start_time).total_seconds() / 60  # duration in minutes
        total_active_minutes += duration
    
    return total_active_minutes

def main():
    # Initialize dictionary to store totals for each project
    project_totals = {}

    # Iterate through all JSON files (projects)
    for file_path in project_files:
        project_name = os.path.basename(file_path).split('_')[0]  # Extract project name from file name
        monthly_active_minutes = 0
        yearly_active_minutes = 0
        
        # Load times from the current project JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Iterate through the days and calculate total active time for each
        for day in data['days']:
            total_active_minutes = calculate_total_active_time(day)
            monthly_active_minutes += total_active_minutes  # Accumulate for the month
            yearly_active_minutes += total_active_minutes  # Accumulate for the year

            total_active_hours = total_active_minutes // 60
            remaining_minutes = total_active_minutes % 60
            day['total_active_time'] = {
                "hours": int(total_active_hours),
                "minutes": int(remaining_minutes)
            }

        # Calculate total active time for the month
        monthly_active_hours = monthly_active_minutes // 60
        monthly_remaining_minutes = monthly_active_minutes % 60

        # Calculate total active time for the year
        yearly_active_hours = yearly_active_minutes // 60
        yearly_remaining_minutes = yearly_active_minutes % 60

        # Store project totals in the dictionary
        project_totals[project_name] = {
            "monthly_total_active_time": {
                "hours": int(monthly_active_hours),
                "minutes": int(monthly_remaining_minutes)
            },
            "yearly_total_active_time": {
                "hours": int(yearly_active_hours),
                "minutes": int(yearly_remaining_minutes)
            }
        }

        # Add monthly and yearly totals to the project data
        data['monthly_total_active_time'] = project_totals[project_name]['monthly_total_active_time']
        data['yearly_total_active_time'] = project_totals[project_name]['yearly_total_active_time']

        # Write the updated data back to the project JSON file with 2 spaces indentation
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    # Print totals for each project
    for project, totals in project_totals.items():
        print(f"Project: {project}")
        print(f"Monthly Total Active Time: {totals['monthly_total_active_time']['hours']} hours and {totals['monthly_total_active_time']['minutes']} minutes")
        print(f"Yearly Total Active Time: {totals['yearly_total_active_time']['hours']} hours and {totals['yearly_total_active_time']['minutes']} minutes")
        print("--------------------------------------------------")
        
