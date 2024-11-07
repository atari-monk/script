import os
import datetime

# Constants
DATABASE_FOLDER = "C:/atari-monk/code/apollo/content/Database"
LOG_FILE_NAME = "log_step.txt"
LOG_FILE_PAHT = os.path.join(DATABASE_FOLDER, LOG_FILE_NAME)
WELCOME_MESSAGE = "Welcome to the Step Logger!"
EXIT_COMMAND = 'exit'

# Function to log steps
def log_step(step):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {step}\n"
    
    # Append the log entry to a log file
    with open(LOG_FILE_PAHT, "a") as log_file:
        log_file.write(log_entry)

    print(f"Logged: {log_entry.strip()}")

# Main routine to log steps
def main():
    print(WELCOME_MESSAGE)
    while True:
        step = input("Enter the step you completed (or type 'exit' to quit): ")
        if step.lower() == EXIT_COMMAND:
            print("Exiting the logger.")
            break
        log_step(step)
