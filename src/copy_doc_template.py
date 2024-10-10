import os
import pyperclip

# Folder path constant
FOLDER_PATH = "./../data/documentation_template"  # Replace with the actual path

def load_md_files(folder):
    """Loads all markdown (.md) files from the specified folder into a dictionary."""
    md_files = {}
    for filename in os.listdir(folder):
        if filename.endswith(".md"):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                md_files[filename] = content
    return md_files

def display_md_files(md_files):
    """Displays the names of all markdown files loaded."""
    print("Loaded Markdown files:")
    for i, filename in enumerate(md_files.keys(), start=1):
        print(f"{i}. {filename}")

def input_file_number(md_files):
    """Prompts the user to input the number corresponding to the markdown file they want to select."""
    try:
        selected_index = int(input("Enter the number of the markdown file to load its content into clipboard: ")) - 1
        if 0 <= selected_index < len(md_files):
            return list(md_files.keys())[selected_index]
        else:
            print("Invalid number selected.")
            return None
    except ValueError:
        print("Please enter a valid number.")
        return None

def main():
    # Load markdown files from the constant folder path
    if not os.path.isdir(FOLDER_PATH):
        print(f"Invalid folder path: {FOLDER_PATH}")
        return
    
    # Load markdown files
    md_files = load_md_files(FOLDER_PATH)
    
    if not md_files:
        print("No markdown files found in the folder.")
        return
    
    # Display the loaded files
    display_md_files(md_files)
    
    # Get user input for file selection by number
    selected_filename = input_file_number(md_files)
    if selected_filename:
        # Copy the content of the selected file to the clipboard
        pyperclip.copy(md_files[selected_filename])
        print(f"The content of '{selected_filename}' has been copied to the clipboard.")

if __name__ == "__main__":
    main()
