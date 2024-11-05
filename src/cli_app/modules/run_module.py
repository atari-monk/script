# main.py or a separate file for better organization

from base.base_module import BaseModule

class RunModule(BaseModule):
    def initialize(self):
        """
        Main loop to run the CLI app, taking user input and executing commands.
        """
        print("Welcome to the CLI App. Type 'help' for a list of commands.")
        
        while self.app.running:
            try:
                user_input = input("CLI> ").strip().split()
                if not user_input:
                    continue

                command, *args = user_input
                if command in self.app.commands:
                    self.app.commands[command](*args)
                else:
                    print(f"Unknown command: {command}. Type 'help' to see available commands.")
            except Exception as e:
                print(f"An error occurred: {e}")
