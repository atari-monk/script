#!/usr/bin/env python3
from __future__ import annotations
import sys
import pyperclip
from pathlib import Path
from typing import List, Optional
from datetime import datetime

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

def add_snippet(content: str, description: Optional[str] = None) -> None:
    snippets: List[str] = load_snippets()
    
    # Build snippet with metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata_parts = [f"Timestamp: {timestamp}"]
    
    if description:
        metadata_parts.append(f"Description: {description}")
    
    # Add metadata header
    metadata = " | ".join(metadata_parts)
    snippet_with_metadata = f"--- {metadata} ---\n{content}"
    
    snippets.append(snippet_with_metadata)
    save_snippets(snippets)
    print(f"Snippet saved. Total snippets: {len(snippets)}")

def print_snippets() -> None:
    snippets: List[str] = load_snippets()
    if not snippets:
        print("No snippets stored.")
        return
    print("Stored snippets:")
    for i, snip in enumerate(snippets, start=1):
        # Extract first line (metadata) for display
        lines = snip.split('\n')
        metadata = lines[0] if lines else ""
        # Get content preview (excluding metadata)
        content_start = snip.find('---', snip.find('---') + 3) + 3 if '---' in snip else 0
        content = snip[content_start:].strip() if content_start > 3 else snip
        preview: str = content.replace("\r", "").replace("\n", " ")[:50]
        print(f"[{i}] {metadata}")
        print(f"    Preview: {preview}...")
        print()

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
    print("Usage: pop.py [command] [options]")
    print("\nCommands:")
    print("  snippet           Add content to stash (default if no args)")
    print("  print             Show all snippets in stash")
    print("  pop [prompt]      Copy snippets + optional prompt to clipboard (stash intact)")
    print("  clear             Clear the stash file manually")
    print("  store             Show stash file path")
    print("\nSnippet command options:")
    print("  -f, --file PATH       Read content from file instead of clipboard")
    print("  -d, --desc TEXT       Description of the snippet")
    print("  -h, --help           Show this help message")
    print("\nExamples:")
    print("  pop.py snippet                        # Add clipboard content")
    print("  pop.py snippet -d \"config example\"    # Add clipboard with description")
    print("  pop.py snippet -f script.py           # Add file content")
    print("  pop.py snippet -f data.txt -d \"data\" # Add file with description")

def main() -> None:
    # Check if first argument is a flag (starts with -)
    if len(sys.argv) == 1:
        # Default: use clipboard
        content: str = pyperclip.paste()
        add_snippet(content)
        return
    
    # If first argument starts with -, treat it as snippet command with flags
    if sys.argv[1].startswith('-'):
        # Parse snippet arguments directly
        file_path = None
        description = None
        
        i = 1  # Start from first argument since there's no "snippet" command
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg in ("-f", "--file") and i + 1 < len(sys.argv):
                file_path = Path(sys.argv[i + 1])
                i += 2
            elif arg in ("-d", "--desc") and i + 1 < len(sys.argv):
                description = sys.argv[i + 1]
                i += 2
            elif arg in ("-h", "--help"):
                show_help()
                return
            else:
                print(f"Unknown option: {arg}")
                show_help()
                return
        
        if file_path:
            # Read content from file
            try:
                if file_path.exists():
                    content = file_path.read_text(encoding="utf-8")
                    add_snippet(content, description)
                else:
                    print(f"Error: File {file_path} does not exist.")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            # Use clipboard content
            content: str = pyperclip.paste()
            add_snippet(content, description)
        return

    command: str = sys.argv[1].lower()
    
    if command in ("-h", "--help"):
        show_help()
    elif command == "snippet":
        # Parse snippet arguments
        file_path = None
        description = None
        
        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg in ("-f", "--file") and i + 1 < len(sys.argv):
                file_path = Path(sys.argv[i + 1])
                i += 2
            elif arg in ("-d", "--desc") and i + 1 < len(sys.argv):
                description = sys.argv[i + 1]
                i += 2
            elif arg in ("-h", "--help"):
                show_help()
                return
            else:
                print(f"Unknown option: {arg}")
                show_help()
                return
        
        if file_path:
            # Read content from file
            try:
                if file_path.exists():
                    content = file_path.read_text(encoding="utf-8")
                    add_snippet(content, description)
                else:
                    print(f"Error: File {file_path} does not exist.")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        else:
            # Use clipboard content
            content: str = pyperclip.paste()
            add_snippet(content, description)
            
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