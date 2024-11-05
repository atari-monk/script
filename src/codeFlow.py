import json
import time
from datetime import datetime, timedelta

LOG_FILE = '../data/refactor_log.json'
TASKS_FILE = '../data/tasks.json'
DEFAULT_SESSION_MINUTES = 25

def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
            priority_order = {"High": 1, "Medium": 2, "Low": 3}
            return sorted(tasks, key=lambda x: priority_order.get(x['priority'], 3))
    except FileNotFoundError:
        return []

def log_entry(entry):
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Error logging entry: {e}")

def load_log():
    try:
        with open(LOG_FILE, 'r') as f:
            return [json.loads(line) for line in f]
    except FileNotFoundError:
        return []

def log_task(task, status, start_time, end_time=None, additional_info=None):
    entry = {
        "task": task,
        "status": status,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat() if end_time else None,
        "additional_info": additional_info
    }
    log_entry(entry)

def display_progress():
    log = load_log()
    completed_tasks = [entry for entry in log if entry['status'] == 'completed']
    interrupted_tasks = [entry for entry in log if entry['status'] == 'interrupted']
    
    print("\n📈 Progress Review:")
    print(f"Total tasks completed: {len(completed_tasks)}")
    print(f"Total interruptions: {len(interrupted_tasks)}\n")
    
    if completed_tasks:
        print("✅ Completed Tasks:")
        for entry in completed_tasks:
            print(f"  - {entry['task']} at {entry['timestamp']}")
    
    if interrupted_tasks:
        print("\n⏸️ Interrupted Tasks:")
        for entry in interrupted_tasks:
            print(f"  - {entry['task']} at {entry['timestamp']}: {entry['additional_info']}")

def provide_focus_tip():
    tips = [
        "🔍 Focus Tip: Keep distractions at a minimum. Set a goal for this session.",
        "🔍 Focus Tip: Take deep breaths if you feel overwhelmed, and focus on one step at a time.",
        "🔍 Focus Tip: Visualize the result you want to achieve by the end of this session."
    ]
    print(tips[int(time.time()) % len(tips)])

def create_tasks():
    tasks = []
    print("Enter tasks (type 'done' when finished):")
    
    while True:
        description = input("Task description: ").strip()
        if description.lower() == 'done':
            break
        priority = input("Priority (High, Medium, Low): ").strip().capitalize()
        if priority not in {"High", "Medium", "Low"}:
            print("Invalid priority. Please enter 'High', 'Medium', or 'Low'.")
            continue
        duration = input(f"Duration in minutes (default {DEFAULT_SESSION_MINUTES}): ").strip()
        try:
            duration = int(duration) if duration else DEFAULT_SESSION_MINUTES
        except ValueError:
            print("Invalid duration. Setting to default.")
            duration = DEFAULT_SESSION_MINUTES

        tasks.append({"description": description, "priority": priority, "duration": duration})
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    print(f"Tasks saved to {TASKS_FILE}.")

def flow_state_cli():
    if input("Do you want to add tasks? (y/n) ").lower() == 'y':
        create_tasks()

    tasks = load_tasks()
    print("🔍 Loading tasks...")

    for task in tasks:
        task_duration = task.get("duration", DEFAULT_SESSION_MINUTES)
        print(f"\n🎯 Task: {task['description']} (Priority: {task['priority']}, Duration: {task_duration} minutes)")
        input("Press Enter to start...")
        
        provide_focus_tip()  # Display a focus tip
        session_start = datetime.now()
        log_task(task['description'], "started", session_start)
        
        print("Stay focused! Avoid distractions. Type 'interrupt' or 'pause' anytime.")
        time_spent = timedelta()
        session_duration = timedelta(minutes=task_duration)
        paused_time = timedelta()
        is_paused = False
        
        while time_spent < session_duration:
            time.sleep(60)
            if not is_paused:
                time_spent = datetime.now() - session_start - paused_time
                print(f"⏳ Time elapsed: {time_spent} / {session_duration}")
            
            user_input = input("Continue, 'pause' to pause, 'interrupt' to log interruption, 'review' to see progress: ").strip().lower()
            if user_input == "interrupt":
                interruption_details = input("Describe the interruption: ")
                log_task(task['description'], "interrupted", session_start, datetime.now(), interruption_details)
                print("Interruption logged. Take a moment to refocus and restart the task.")
                break
            elif user_input == "pause":
                if is_paused:
                    is_paused = False
                    resume_time = datetime.now()
                    paused_time += resume_time - pause_start
                    print("Resuming task.")
                else:
                    is_paused = True
                    pause_start = datetime.now()
                    print("Task paused. Type 'pause' again to resume.")
            elif user_input == "review":
                display_progress()
        
        else:
            print("Session complete! Take a short break.")
            log_task(task['description'], "completed", session_start, datetime.now())
        
        if input("Start next task? (y/n) ").lower() != 'y':
            break

    display_progress()
    print("✅ All tasks completed. Great work!")

if __name__ == "__main__":
    flow_state_cli()
