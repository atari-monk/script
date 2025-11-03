# Tree

Py script to print file system tree

It takes path:

```py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

print(f"Path: {args.path}")
```

and prints out tree structure of files in that path  
We must ignore some folders and files

//Key with names are just for user information, in script we ignore all

```json
{
	"files": {
		"vite-ts": []
	},
	"folders": {
		"vanilla-js": [],
		"vite-ts": []
	}
}
```

Therfore we should load these for json data in above format

We should put it in clipboard if flag -c is given
Use proper flag notations for argparse
Use procedural coding style - data, functions
We should use main as this is for console entry point

Script Code:

```py
import argparse
import os
import json
import pyperclip
from pathlib import Path

# Data
config = {
    "files": {
        "vite-ts": [],
        "vanilla-js": []
    },
    "folders": {
        "vite-ts": ["node_modules", "dist", ".git"],
        "vanilla-js": []
    }
}

# Load config from JSON file if exists
def load_config():
    global config
    config_files = [".treeignore", "tree_config.json", "config.json"]

    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with default config
                    if "files" in loaded_config:
                        # Update each category individually
                        for category, patterns in loaded_config["files"].items():
                            if category in config["files"]:
                                config["files"][category] = patterns
                            else:
                                config["files"][category] = patterns

                    if "folders" in loaded_config:
                        # Update each category individually
                        for category, patterns in loaded_config["folders"].items():
                            if category in config["folders"]:
                                config["folders"][category] = patterns
                            else:
                                config["folders"][category] = patterns

                print(f"Loaded config from {config_file}")
                break
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error loading {config_file}: {e}")

# Functions
def get_ignore_patterns():
    """Extract all ignore patterns from config"""
    ignore_folders = set()
    ignore_files = set()

    # Collect all folder patterns from all categories
    for category, folders in config.get("folders", {}).items():
        ignore_folders.update(folders)

    # Collect all file patterns from all categories
    for category, files in config.get("files", {}).items():
        ignore_files.update(files)

    return ignore_folders, ignore_files

def should_ignore(name, is_folder=True):
    """Check if a file/folder should be ignored"""
    ignore_folders, ignore_files = get_ignore_patterns()

    if is_folder and name in ignore_folders:
        return True
    if not is_folder and name in ignore_files:
        return True

    return False

def get_tree_structure(path, prefix="", is_last=True, level=0, max_level=None):
    """Generate tree structure recursively"""
    if max_level is not None and level >= max_level:
        return ""

    path = Path(path)
    if not path.exists():
        return f"Path does not exist: {path}"

    # Get all items, sorted and filtered
    try:
        items = []
        for item in path.iterdir():
            if item.is_dir() and should_ignore(item.name, is_folder=True):
                continue
            if item.is_file() and should_ignore(item.name, is_folder=False):
                continue
            items.append(item)

        # Sort: folders first, then files, both alphabetically
        items.sort(key=lambda x: (x.is_file(), x.name.lower()))

    except PermissionError:
        return f"{prefix}└── [Permission Denied]"

    if not items:
        return ""

    tree_lines = []
    connector = "└── " if is_last else "├── "

    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        new_prefix = prefix + ("    " if is_last else "│   ")

        if item.is_dir():
            tree_lines.append(f"{prefix}{connector}{item.name}/")
            subtree = get_tree_structure(
                item,
                new_prefix,
                is_last_item,
                level + 1,
                max_level
            )
            if subtree:
                tree_lines.append(subtree)
        else:
            tree_lines.append(f"{prefix}{connector}{item.name}")

    return "\n".join(tree_lines)

def generate_tree(path, max_level=None):
    """Generate complete tree structure"""
    path = Path(path).resolve()

    if not path.exists():
        return f"Error: Path does not exist - {path}"

    if path.is_file():
        return path.name

    tree_lines = [f"{path.name}/"]
    tree_structure = get_tree_structure(path, max_level=max_level)

    if tree_structure:
        tree_lines.append(tree_structure)

    return "\n".join(tree_lines)

def main():
    # Load configuration
    load_config()

    # Argument parser
    parser = argparse.ArgumentParser(description='Print file system tree structure')
    parser.add_argument('path', nargs='?', default='.', help='Path to generate tree for (default: current directory)')
    parser.add_argument('-c', '--clipboard', action='store_true',
                       help='Copy tree to clipboard instead of printing')
    parser.add_argument('-l', '--level', type=int, default=None,
                       help='Maximum depth level to display')
    parser.add_argument('-s', '--show-ignore', action='store_true',
                       help='Show what patterns are being ignored')

    args = parser.parse_args()

    # Show ignore patterns if requested
    if args.show_ignore:
        ignore_folders, ignore_files = get_ignore_patterns()
        print("Current ignore patterns:")
        print(f"Folders: {sorted(ignore_folders)}")
        print(f"Files: {sorted(ignore_files)}")
        print(f"\nConfig structure:")
        print(json.dumps(config, indent=2))
        return

    # Display loaded ignore patterns (for user information)
    ignore_folders, ignore_files = get_ignore_patterns()
    if ignore_folders or ignore_files:
        print("Ignore patterns loaded:")
        if ignore_folders:
            print(f"  Folders: {', '.join(sorted(ignore_folders))}")
        if ignore_files:
            print(f"  Files: {', '.join(sorted(ignore_files))}")
        print()

    # Generate tree
    tree_output = generate_tree(args.path, max_level=args.level)

    # Handle output
    if args.clipboard:
        try:
            pyperclip.copy(tree_output)
            print("Tree structure copied to clipboard!")
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
    else:
        # Default behavior: print to console
        print(tree_output)

if __name__ == "__main__":
    main()
```

Usage:

```py
# Print tree of current directory (default)
fstree

# Print tree of specific directory
fstree /path/to/directory

# Copy tree to clipboard instead of printing
fstree -c
fstree --clipboard

# Show ignore patterns
fstree -s
fstree --show-ignore

# Limit depth
fstree -l 2
fstree --level 3
```
