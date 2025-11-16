#!/usr/bin/env python3
from __future__ import annotations
import sys
import pyperclip
from pathlib import Path
from typing import List, Optional

SNIPPET_FILE: Path = Path("/tmp/all_snippets.txt")
SEPARATOR: str = "\n\n===SNIPPET===\n\n"

def load_snippets() -> List[str]:
    if not SNIPPET_FILE.exists():
        return []
    content = SNIPPET_FILE.read_text(encoding="utf-8")
    snippets = [s for s in content.split(SEPARATOR) if s.strip()]
    return snippets

def save_snippets(snippets: List[str]) -> None:
    with SNIPPET_FILE.open("w", encoding="utf-8", newline="") as f:
        f.write(SEPARATOR.join(snippets))

def add_snippet(content: str) -> None:
    snippets: List[str] = load_snippets()
    snippets.append(content)
    save_snippets(snippets)
    print(f"Snippet saved. Total snippets: {len(snippets)}")

def print_snippets() -> None:
    snippets: List[str] = load_snippets()
    if not snippets:
        print("No snippets stored.")
        return
    print("Stored snippets:")
    for i, snip in enumerate(snippets, start=1):
        preview: str = snip.replace("\r", "").replace("\n", " ")[:50]
        print(f"[{i}] {preview}...")

def pop_snippets(prompt: Optional[str] = None) -> None:
    """Copy all snippets + optional prompt to clipboard without clearing stash."""
    snippets: List[str] = load_snippets()
    if not snippets:
        print("No snippets to pop.")
        return
    combined: str = "\n\n".join(snippets)
    if prompt:
        combined += f"\n\n{prompt}"
    pyperclip.copy(combined)
    print(f"Combined {len(snippets)} snippet(s) copied to clipboard (stash intact).")

def clear_stash() -> None:
    """Clear the stash file manually."""
    SNIPPET_FILE.unlink(missing_ok=True)
    print("Snippet stash has been cleared.")

def show_store_path() -> None:
    """Print the path to the stash file."""
    print(f"Snippet stash file: {SNIPPET_FILE.resolve()}")

def show_help() -> None:
    print("Usage: pop.py [command] [prompt]")
    print("Commands:")
    print("  snippet      Add clipboard content to stash (default if no args)")
    print("  print        Show all snippets in stash")
    print("  pop [prompt] Copy snippets + optional prompt to clipboard (stash intact)")
    print("  clear        Clear the stash file manually")
    print("  store        Show stash file path")
    print("Flags:")
    print("  -h, --help   Show this help message")

def main() -> None:
    if len(sys.argv) < 2:
        content: str = pyperclip.paste()
        add_snippet(content)
        return

    command: str = sys.argv[1].lower()
    if command in ("-h", "--help"):
        show_help()
    elif command == "snippet":
        content: str = pyperclip.paste()
        add_snippet(content)
    elif command == "print":
        print_snippets()
    elif command == "pop":
        prompt: Optional[str] = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        pop_snippets(prompt)
    elif command == "clear":
        clear_stash()
    elif command == "store":
        show_store_path()
    else:
        print(f"Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()
