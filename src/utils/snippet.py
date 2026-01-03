#!/usr/bin/env python3
from __future__ import annotations
import sys
from .clipboard_utils import copy_to_clipboard, paste_from_clipboard
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

SNIPPET_FILE: Path = Path("/tmp/all_snippets.txt")
SEPARATOR: str = "\n\n===SNIPPET===\n\n"
VALID_TYPES: List[str] = ["context", "task", "prompt", "generic"]


# ------------------------------------------------------------
# Storage helpers
# ------------------------------------------------------------

def load_snippets() -> List[str]:
    if not SNIPPET_FILE.exists():
        return []
    content: str = SNIPPET_FILE.read_text(encoding="utf-8")
    return [s for s in content.split(SEPARATOR) if s.strip()]


def save_snippets(snippets: List[str]) -> None:
    SNIPPET_FILE.write_text(SEPARATOR.join(snippets), encoding="utf-8")


# ------------------------------------------------------------
# Snippet creation
# ------------------------------------------------------------

def add_snippet(
    content: str,
    description: Optional[str] = None,
    stype: Optional[str] = None
) -> None:
    snippets: List[str] = load_snippets()

    timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    meta: List[str] = [f"Timestamp: {timestamp}"]

    if description:
        meta.append(f"Description: {description}")

    if stype in VALID_TYPES:
        meta.append(f"Type: {stype}")
    else:
        meta.append("Type: generic")

    metadata: str = " | ".join(meta)
    snippet_with_meta: str = f"--- {metadata} ---\n{content}"

    snippets.append(snippet_with_meta)
    save_snippets(snippets)

    print(f"Snippet saved. Total snippets: {len(snippets)}")


# ------------------------------------------------------------
# Pretty-print stored snippets
# ------------------------------------------------------------

def print_snippets() -> None:
    snippets: List[str] = load_snippets()
    if not snippets:
        print("No snippets stored.")
        return

    print("Stored snippets:\n")
    for i, snip in enumerate(snippets, start=1):
        lines: List[str] = snip.split("\n")
        metadata: str = lines[0] if lines else ""

        # Extract content after metadata block
        content_start: int = snip.find("---", snip.find("---") + 3) + 3
        preview_block: str = snip[content_start:].strip() if content_start > 3 else snip
        preview: str = preview_block.replace("\r", "").replace("\n", " ")[:50]

        print(f"[{i}] {metadata}")
        print(f"    Preview: {preview}...\n")


# ------------------------------------------------------------
# POP — generate structured prompt
# ------------------------------------------------------------

def pop_snippets(prompt: Optional[str] = None) -> None:
    snippets: List[str] = load_snippets()
    if not snippets:
        print("No snippets to pop.")
        return

    context: List[str] = []
    task: List[str] = []
    prompts: List[str] = []
    generic: List[str] = []

    # classify snippets
    for snip in snippets:
        header_end: int = snip.find("\n")
        header: str = snip[:header_end] if header_end > 0 else snip

        if "Type: context" in header:
            context.append(snip)
        elif "Type: task" in header:
            task.append(snip)
        elif "Type: prompt" in header:
            prompts.append(snip)
        else:
            generic.append(snip)

    blocks: List[str] = []

    if context:
        blocks.append("### CONTEXT\n" + "\n\n".join(context))
    if task:
        blocks.append("### TASK\n" + "\n\n".join(task))
    if generic:
        blocks.append("### MISC\n" + "\n\n".join(generic))
    if prompts:
        blocks.append("### PROMPTS\n" + "\n\n".join(prompts))
    if prompt:
        blocks.append("### DIRECT PROMPT\n" + prompt)

    final_text: str = "\n\n".join(blocks)

    copy_to_clipboard(final_text)
    print("Structured prompt copied to clipboard.")


# ------------------------------------------------------------
# Misc utilities
# ------------------------------------------------------------

def clear_stash() -> None:
    SNIPPET_FILE.unlink(missing_ok=True)
    print("Snippet stash cleared.")


def show_store_path() -> None:
    print(f"Snippet stash file: {SNIPPET_FILE.resolve()}")


# ------------------------------------------------------------
# Help
# ------------------------------------------------------------

def show_help() -> None:
    print("Usage: snippet [command] [options]\n")
    print("Commands:")
    print("  print                 Show all stored snippets")
    print("  pop [prompt]          Build structured prompt")
    print("  clear                 Clear snippet stash")
    print("  store                 Show stash path\n")
    print("When no command is provided, a snippet is added from the clipboard.\n")
    print("Snippet options (these add a snippet):")
    print("  -f, --file PATH       Read content from file")
    print("  -c, --content TEXT    Use TEXT as snippet content")
    print("  -d, --desc TEXT       Add a description")
    print("  -t, --type TYPE       context | task | prompt | generic\n")
    print("Examples:")
    print("  snippet                     (from clipboard)")
    print("  snippet -c \"hello world\"")
    print("  snippet -f utils.ts -t context")
    print("  snippet pop \"Explain this code\"")


# ------------------------------------------------------------
# CLI dispatcher (rewritten)
# ------------------------------------------------------------

def main() -> None:
    argv: List[str] = sys.argv

    # ------------------------------------------------------------
    # No args: add clipboard snippet
    # ------------------------------------------------------------
    if len(argv) == 1:
        content = paste_from_clipboard()
        add_snippet(content, None, None)
        return

    command = argv[1]

    # ------------------- Commands ------------------------------

    if command in ("-h", "--help"):
        show_help()
        return

    if command == "print":
        print_snippets()
        return

    if command == "pop":
        prompt = " ".join(argv[2:]) if len(argv) > 2 else None
        pop_snippets(prompt)
        return

    if command == "clear":
        clear_stash()
        return

    if command == "store":
        show_store_path()
        return

    # ------------------------------------------------------------
    # Options-only mode = add snippet
    # ------------------------------------------------------------
    if command.startswith("-"):
        file_path: Optional[Path] = None
        description: Optional[str] = None
        stype: Optional[str] = None
        direct_content: Optional[str] = None

        i = 1
        while i < len(argv):
            arg = argv[i]

            if arg in ("-f", "--file") and i + 1 < len(argv):
                file_path = Path(argv[i + 1])
                i += 2
                continue

            if arg in ("-c", "--content") and i + 1 < len(argv):
                direct_content = argv[i + 1]
                i += 2
                continue

            if arg in ("-d", "--desc") and i + 1 < len(argv):
                description = argv[i + 1]
                i += 2
                continue

            if arg in ("-t", "--type") and i + 1 < len(argv):
                stype = argv[i + 1]
                i += 2
                continue

            if arg.startswith("-"):
                print(f"Unknown option: {arg}")
                show_help()
                return

            i += 1

        # Load snippet content
        if direct_content is not None:
            content = direct_content
        elif file_path is not None:
            if not file_path.exists():
                print(f"Error: File does not exist: {file_path}")
                return
            content = file_path.read_text(encoding="utf-8")
        else:
            content = paste_from_clipboard()

        add_snippet(content, description, stype)
        return

    # ------------------------------------------------------------
    # Unknown command
    # ------------------------------------------------------------
    print(f"Unknown command: {command}")
    show_help()


# ------------------------------------------------------------

if __name__ == "__main__":
    main()
