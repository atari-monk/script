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
                
                # Check if the command is a number and map it to the corresponding command
                if command.isdigit():
                    command_number = int(command)
                    command_found = False
                    
                    # Find the command by its number
                    for item in self.app.context.last_menu:
                        if item['number'] == command_number:
                            command = item['command']
                            command_found = True
                            break
                    
                    if not command_found:
                        print(f"No command found for number: {command_number}")
                        continue

                # Execute the command if it's valid
                if command in self.app.context.commands:
                    self.app.context.execute_command(command, *args)
                else:
                    print(f"Unknown command: {command}. Type 'help' to see available commands.")
            except Exception as e:
                print(f"An error occurred: {e}")
