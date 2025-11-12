#!/usr/bin/env python3
import subprocess
from pathlib import Path

def is_git_repo(path: Path) -> bool:
    return (path / ".git").is_dir()

def check_uncommitted(path: Path):
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout.strip():
            print(f"[{path}] has uncommitted changes:")
            print(result.stdout)
        else:
            print(f"[{path}] is clean.")
    except subprocess.CalledProcessError:
        print(f"[{path}] is not a Git repository.")

def main():
    base_path = Path(".")  # current folder
    for subfolder in base_path.iterdir():
        if subfolder.is_dir() and is_git_repo(subfolder):
            check_uncommitted(subfolder)

if __name__ == "__main__":
    main()
