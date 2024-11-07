import json
import os
from datetime import datetime

# Define project_files as a dictionary, not a set
project_files = {
    "morpheus": '../../data/morpheus_time_logger.json'
}

# Function to validate date format
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to validate time format
def validate_time(time_text):
    try:
        datetime.strptime(time_text, "%H:%M")
        return True
    except ValueError:
        return False

# Function to input session times
def input_sessions():
    sessions = []
    while True:
        start_time = input("Enter session start time (HH:MM) or 'done' to finish: ")
        if start_time.lower() == 'done':
            break
        if not validate_time(start_time):
            print("Invalid time format. Please enter in HH:MM format.")
            continue

        end_time = input("Enter session end time (HH:MM): ")
        if not validate_time(end_time):
            print("Invalid time format. Please enter in HH:MM format.")
            continue

        # Add session to list
        sessions.append({"start": start_time, "end": end_time})
    
    return sessions

# Function to load or create project file
def load_or_create_project_file(project_name):
    if project_name in project_files:
        project_file_path = project_files[project_name]
    else:
        # If project doesn't exist, create a new file path
        project_file_path = f'../../data/{project_name.lower().replace(" ", "_")}_schedule.json'
        project_files[project_name] = project_file_path
    
    if os.path.exists(project_file_path):
        with open(project_file_path, 'r') as file:
            return json.load(file), project_file_path
    else:
        return {"days": []}, project_file_path  # New project file

# Main function to gather input and save to JSON
def add_day_to_project():
    print("Select a project or create a new one:")
    for i, project_name in enumerate(project_files.keys(), 1):
        print(f"{i}. {project_name}")
    
    project_choice = input("Enter the number of the project or a new project name: ")
    
    if project_choice.isdigit() and 1 <= int(project_choice) <= len(project_files):
        project_name = list(project_files.keys())[int(project_choice) - 1]
    else:
        project_name = project_choice  # Treat as new project
    
    # Load or create project data
    project_data, project_file_path = load_or_create_project_file(project_name)

    # Get the date for the new entry
    while True:
        date_to_add = input("Enter the date for the new entry (YYYY-MM-DD): ")
        if validate_date(date_to_add):
            break
        else:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")

    # Input session times
    sessions = input_sessions()

    if not sessions:
        print("No sessions were added. Exiting.")
        return

    # Add the new day to the project
    new_day = {
        "date": date_to_add,
        "sessions": sessions
    }

    # Append the new day to the list
    project_data['days'].append(new_day)

    # Save the updated project data to the JSON file
    with open(project_file_path, 'w') as file:
        json.dump(project_data, file, indent=2)

    print(f"Data for {date_to_add} added to {project_name} and saved to {project_file_path}")

def main():
    add_day_to_project()
