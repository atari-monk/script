import tkinter as tk
from tkinter import messagebox
import time

reminder_rules = [
    {"Title": "Sleep", "Rule": "1. It's 23:00 go sleep.", "hour": 23, "minutes": 0, "reminder_count": 1, "current_reminder_count": 0},
]

def reminder(title, rule):
    messagebox.showinfo(title, rule)

def check_reminder(root):
    current_time = time.localtime()

    print(f"Current Time: {current_time.tm_hour}:{current_time.tm_min}")

    for rule in reminder_rules:
        if (
            current_time.tm_hour > rule["hour"]
            or (current_time.tm_hour == rule["hour"] and current_time.tm_min >= rule["minutes"])
        ):
            if rule["current_reminder_count"] < rule["reminder_count"]:
                reminder(rule["Title"], rule["Rule"])
                rule["current_reminder_count"] += 1

    root.after(60000, check_reminder)

def main():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Reminder", "Time Watcher on")

    check_reminder(root)

    root.mainloop()
