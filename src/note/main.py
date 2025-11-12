import sys
from typing import Dict, Callable
from note.utils import log

STORE: Dict[str, Callable[[str], None]] = {
    'note': lambda note: log('C:/Atari-Monk/data/docs/note.txt', note),
}

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