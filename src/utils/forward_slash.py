import pyperclip

def convert_path_slashes(path: str) -> str:
    """
    Convert all backslashes in a path to forward slashes.
    """
    return path.replace("\\", "/")

def main() -> None:
    # Read path from clipboard
    path = pyperclip.paste()
    # Convert backslashes to forward slashes
    converted = convert_path_slashes(path)
    # Put back into clipboard
    pyperclip.copy(converted)
    print(f"✅ Converted path copied to clipboard:\n{converted}")

if __name__ == "__main__":
    main()
