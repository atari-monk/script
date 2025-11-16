import sys
from typing import Dict, Callable
from datetime import datetime as dt
import subprocess

STORE: Dict[str, Callable[[str], None]] = {
    'note': lambda note: log('C:/Atari-Monk/data/docs/note.txt', note),
}

def pad_two(number: int) -> str:
    return f"0{number}" if number < 10 else str(number)

def get_datetime() -> str:
    now = dt.now()
    date_part = f"{now.year}-{pad_two(now.month)}-{pad_two(now.day)}"
    time_part = f"{pad_two(now.hour)}:{pad_two(now.minute)}"
    return f"{date_part} {time_part}"

def copy_to_clipboard(text:str):
    subprocess.run("clip", text=True, input=text, shell=True)

def get_input(prompt: str = "") -> str:
    if prompt:
        print(prompt)
    return input().strip()

def append_to_file(file_path: str, text: str):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(text + '\n')

def log(file_path: str, note: str, copy:bool = False):
    datetime = get_datetime()
    log = f"{datetime} {note}".lower()
    print(log)
    if copy:
        copy_to_clipboard(log)
        print('In clipboard!')
    append_to_file(file_path, log)

def main() -> None:
    
    if len(sys.argv) < 3:
        print(f"Usage: log <project> <note>")
        print(f"Available projects: {list(STORE.keys())}")
        return
    
    project = sys.argv[1]
    note = sys.argv[2]
    
    if project in STORE:
        STORE[project](note)
    else:
        print(f"Unknown project. Available: {list(STORE.keys())}")

if __name__ == "__main__":
    main()