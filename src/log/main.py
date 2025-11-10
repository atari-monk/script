import sys
from typing import Dict, Callable
from log.utils import log

PROJECTS: Dict[str, Callable[[str], None]] = {
    'cv': lambda note: log('C:/Atari-Monk/projects/cv/docs/log.md', note),
    'checkpoint': lambda note: log('C:/Atari-Monk/projects/checkpoint/docs/log.md', note),
    'script': lambda note: log('C:/Atari-Monk/projects/script/docs/log.md', note),
    'blog': lambda note: log('C:/Atari-Monk/projects/blog/docs/log.md', note),
}

def main() -> None:
    
    if len(sys.argv) < 3:
        print(f"Usage: log <project> <note>")
        print(f"Available projects: {list(PROJECTS.keys())}")
        return
    
    project = sys.argv[1]
    note = sys.argv[2]
    
    if project in PROJECTS:
        PROJECTS[project](note)
    else:
        print(f"Unknown project. Available: {list(PROJECTS.keys())}")

if __name__ == "__main__":
    main()