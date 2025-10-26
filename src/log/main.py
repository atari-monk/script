import sys
from log.utils import log

PROJECTS = {
    'cv': lambda note: log('C:/Atari-Monk/cv/docs/log.md', note),
    'checkpoint': lambda note: log('C:/Atari-Monk/checkpoint/docs/log.md', note),
    'script': lambda note: log('C:/Atari-Monk/script/docs/log.md', note),
}

def main():
    
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