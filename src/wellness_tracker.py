import json
import os
from datetime import datetime

DATA_FILE = "wellness_log.json"

# Load or initialize data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"entries": [], "reminders": []}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_entry():
    date = datetime.now().strftime("%Y-%m-%d")
    mood = input("Rate your mood (1-10): ")
    thought = input("What's on your mind today? ")

    entry = {
        "date": date,
        "mood": mood,
        "thought": thought
    }

    data["entries"].append(entry)
    save_data()
    print("Entry saved.")

def view_entries():
    if data["entries"]:
        for entry in data["entries"]:
            print(f"\nDate: {entry['date']}")
            print(f"Mood: {entry['mood']}")
            print(f"Thought: {entry['thought']}")
    else:
        print("No entries found.")

def add_reminder():
    reminder = input("Enter a reminder for yourself: ")
    data["reminders"].append(reminder)
    save_data()
    print("Reminder added.")

def view_reminders():
    if data["reminders"]:
        print("\nYour Reminders:")
        for idx, reminder in enumerate(data["reminders"], start=1):
            print(f"{idx}. {reminder}")
    else:
        print("No reminders found.")

def main():
    while True:
        print("\nWelcome to the Wellness Tracker")
        print("1. Add Daily Entry")
        print("2. View Entries")
        print("3. Add Reminder")
        print("4. View Reminders")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_entry()
        elif choice == "2":
            view_entries()
        elif choice == "3":
            add_reminder()
        elif choice == "4":
            view_reminders()
        elif choice == "5":
            print("Goodbye. Take care.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
