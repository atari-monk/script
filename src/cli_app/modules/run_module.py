from base.base_module import BaseModule

class RunModule(BaseModule):
    def initialize(self):
        """
        Main loop to run the CLI app, taking user input and executing commands.
        """
        print("Welcome to the CLI App. Type 'help' for a list of commands.")

        while self.app.running:
            try:
                user_input = input("CLI> ").strip()
                if not user_input:
                    continue

                # Parse the user input into arguments
                parts = self.parse_input(user_input)
                #print(parts)  # For debugging: print the parsed input

                command = parts[0]
                args = parts[1:]

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

    def parse_input(self, user_input):
        """
        Parse the user input, handling both double and single quoted strings as a single argument.
        Rejects input with unmatched quotes.
        """
        parts = []
        current_arg = []
        inside_quotes = None  # None = not inside quotes, otherwise it holds the quote type (' or ")

        # Loop through each character in the input string
        for char in user_input:
            if char == '"' or char == "'":
                # If inside quotes, check if it's the same quote that started the group
                if inside_quotes == char:
                    # End of the quoted string, push current argument
                    parts.append(''.join(current_arg))
                    current_arg = []
                    inside_quotes = None  # Exit the quoted section
                elif inside_quotes is None:
                    # Start of a quoted string (either ' or ")
                    inside_quotes = char
                else:
                    # Ignore other quotes if already inside quotes
                    current_arg.append(char)
            elif char == ' ' and inside_quotes is None:
                # If not inside quotes, split on spaces
                if current_arg:
                    parts.append(''.join(current_arg))
                    current_arg = []
            else:
                # Collect characters for the current argument
                current_arg.append(char)

        # Add any remaining argument (in case no space at the end)
        if current_arg:
            parts.append(''.join(current_arg))

        # Reject input with unmatched quotes
        if inside_quotes is not None:
            raise ValueError("Error: Unmatched quote detected. Please ensure both quotes are closed.")

        return parts
