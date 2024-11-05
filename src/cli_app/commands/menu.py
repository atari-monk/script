# commands/help.py

import os
from base.base_command import BaseCommand

class MenuCommand(BaseCommand):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.command_list = []  # To store numbered list of commands and folders
        self.ignore_list = {'__init__.py', '__pycache__'}  # Items to ignore

    def execute(self, *args):
        # Determine the main commands folder path
        commands_folder = 'commands'

        # If there is an argument, treat it as a subfolder selection
        if args:
            try:
                choice = int(args[0]) - 1
                selected = self.command_list[choice]
                if selected['type'] == 'folder':
                    self.print_subfolder_commands(selected['name'])
                else:
                    print("Not a folder with commands.")
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a valid number.")
            return

        # Display files and folders in the commands directory
        print("Commands and folders in the 'commands' directory:")
        self.command_list = []  # Reset the command list for each execution
        menu = []  # To store the menu items for the last printed menu
        index = 1

        # List files and folders in the commands directory, ignoring items in ignore_list
        for item in os.listdir(commands_folder):
            if item in self.ignore_list:
                continue  # Skip ignored items

            item_path = os.path.join(commands_folder, item)
            if os.path.isfile(item_path) and item.endswith('.py'):
                # Display Python files as commands, omitting the '.py' extension
                command_name = item[:-3]
                print(f"  {index}. {command_name}")
                self.command_list.append({'name': command_name, 'type': 'command'})
                menu.append({'number': index, 'command': command_name})  # Add to menu list
                index += 1
            elif os.path.isdir(item_path):
                # Display folders as command categories
                print(f"  {index}. {item} (folder)")
                self.command_list.append({'name': item, 'type': 'folder'})
                menu.append({'number': index, 'command': item})  # Add to menu list
                index += 1

        # Store the entire printed menu state
        self.app.context.set_last_menu(menu)

    def print_subfolder_commands(self, folder_name):
        """Print commands within the specified subfolder in the 'commands' directory."""
        folder_path = os.path.join('commands', folder_name)
        if not os.path.isdir(folder_path):
            print(f"No such folder: {folder_name}")
            return

        print(f"\nCommands in the '{folder_name}' folder:")
        menu = []  # To store the menu items for the last printed subfolder menu
        for i, file_name in enumerate(os.listdir(folder_path), start=1):
            # Check for Python files, assuming each file represents a command in the folder
            if file_name.endswith('.py') and file_name not in self.ignore_list:
                command_name = file_name[:-3]  # Remove '.py' extension
                print(f"  {i}. {folder_name}/{command_name}")  # Prefix folder name
                menu.append({'number': i, 'command': f"{folder_name}/{command_name}"})  # Add folder before command name

        # Store the entire printed subfolder menu state
        self.app.context.set_last_menu(menu)

    @property
    def description(self):
        return "Display available commands and folders in the 'commands' directory."
