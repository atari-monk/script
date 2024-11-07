import os
import datetime

# Constants
DATABASE_FOLDER = "C:/atari-monk/code/apollo/content/Database"
LOG_FILE_NAME = "log_goal.txt"
LOG_FILE_PAHT = os.path.join(DATABASE_FOLDER, LOG_FILE_NAME)
WELCOME_MESSAGE = "Welcome to the Goal Logger!"
EXIT_COMMAND = 'exit'

# Function to log goals
def log_goal(goal):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {goal}\n"
    
    # Append the log entry to a log file
    with open(LOG_FILE_PAHT, "a") as log_file:
        log_file.write(log_entry)

    print(f"Logged: {log_entry.strip()}")

# Main routine to log goals
def main():
    print(WELCOME_MESSAGE)
    while True:
        goal = input("Enter your goal (or type 'exit' to quit): ")
        if goal.lower() == EXIT_COMMAND:
            print("Exiting the logger.")
            break
        log_goal(goal)
