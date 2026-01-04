import argparse
import json
import os
from pathlib import Path
from .clipboard_utils import copy_to_clipboard


CONFIG_FILE = "/home/atari-monk/atari-monk/project/script/src/utils/tree.json"

# Default config (used if config.json is missing)
config = {
    "ignore": {
        "folders": [],
        "files": []
    }
}


# ------------------------
# Config
# ------------------------
def load_config():
    global config

    if not os.path.exists(CONFIG_FILE):
        return

    try:
        with open(CONFIG_FILE, "r") as f:
            loaded = json.load(f)

        ignore = loaded.get("ignore", {})
        config["ignore"]["folders"] = ignore.get("folders", [])
        config["ignore"]["files"] = ignore.get("files", [])

        print("Loaded config.json\n")

    except Exception as e:
        print(f"Error loading config.json: {e}")


def should_ignore(path: Path):
    name = path.name
    if path.is_dir():
        return name in config["ignore"]["folders"]
    return name in config["ignore"]["files"]


# ------------------------
# Tree logic
# ------------------------
def build_tree(path, prefix="", level=0, max_level=None):
    if max_level is not None and level >= max_level:
        return []

    try:
        items = [
            p for p in path.iterdir()
            if not should_ignore(p)
        ]
    except PermissionError:
        return [f"{prefix}└── [Permission denied]"]

    items.sort(key=lambda p: (p.is_file(), p.name.lower()))
    lines = []

    for i, item in enumerate(items):
        last = i == len(items) - 1
        connector = "└── " if last else "├── "
        lines.append(f"{prefix}{connector}{item.name}{'/' if item.is_dir() else ''}")

        if item.is_dir():
            extension = "    " if last else "│   "
            lines.extend(
                build_tree(
                    item,
                    prefix + extension,
                    level + 1,
                    max_level
                )
            )

    return lines


def generate_tree(path, max_level=None):
    path = Path(path).resolve()

    if not path.exists():
        return f"Error: {path} does not exist"

    if path.is_file():
        return path.name

    lines = [f"{path.name}/"]
    lines.extend(build_tree(path, max_level=max_level))
    return "\n".join(lines)


# ------------------------
# CLI
# ------------------------
def main():
    load_config()

    parser = argparse.ArgumentParser(description="Print directory tree")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("-l", "--level", type=int, help="Max depth")
    parser.add_argument("-c", "--clipboard", action="store_true")
    parser.add_argument("-s", "--show-ignore", action="store_true")

    args = parser.parse_args()

    if args.show_ignore:
        print(json.dumps(config, indent=2))
        return

    output = generate_tree(args.path, args.level)

    if args.clipboard:
        copy_to_clipboard(output)
        print("Copied to clipboard")
    else:
        print(output)


if __name__ == "__main__":
    main()
