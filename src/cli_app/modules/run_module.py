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

                command, args = self.parse_input(user_input)

                # Map number input to command if applicable
                command = self.get_command_by_number_if_digit(command)

                if command:
                    self.execute_command(command, args)
                else:
                    print(f"Unknown command: {command}. Type 'help' to see available commands.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def get_command_by_number_if_digit(self, command):
        """
        If the command is a digit, attempt to map it to a command from the last menu.
        """
        if command.isdigit():
            return self.get_command_by_number(int(command))
        return command

    def get_command_by_number(self, command_number):
        """
        Find the command by its number from the last menu.
        Returns the command if found, otherwise None.
        """
        for item in self.app.context.last_menu:
            if item['number'] == command_number:
                return item['command']
        return None

    def execute_command(self, command, args):
        """
        Executes the command if it's valid.
        """
        if command in self.app.context.commands:
            self.app.context.execute_command(command, *args)
        else:
            print(f"Unknown command: {command}. Type 'help' to see available commands.")

    def parse_input(self, user_input):
        """
        Parse the user input, handling both double and single quoted strings as a single argument.
        Rejects input with unmatched quotes.
        """
        parts = []
        current_arg = []
        inside_quotes = None

        for char in user_input:
            if char in ('"', "'"):
                self.handle_quotes(char, inside_quotes, current_arg, parts)
                inside_quotes = self.toggle_quotes(char, inside_quotes)
            elif char == ' ' and inside_quotes is None:
                self.add_argument(parts, current_arg)
            else:
                current_arg.append(char)

        self.finalize_argument(parts, current_arg, inside_quotes)

        # If no arguments, return just the command
        if len(parts) == 1:
            return parts[0], []

        return parts[0], parts[1:]

    def handle_quotes(self, char, inside_quotes, current_arg, parts):
        """
        Handles the state change when encountering a quote (either single or double).
        """
        if inside_quotes == char:
            parts.append(''.join(current_arg))
            current_arg.clear()

    def toggle_quotes(self, char, inside_quotes):
        """
        Toggles the state of quote (either starting or ending a quoted section).
        """
        if inside_quotes is None:
            return char
        return None

    def add_argument(self, parts, current_arg):
        """
        Adds the current argument to the parts list when a space is encountered.
        """
        if current_arg:
            parts.append(''.join(current_arg))
            current_arg.clear()

    def finalize_argument(self, parts, current_arg, inside_quotes):
        """
        Finalizes the current argument and ensures no unmatched quotes.
        """
        if current_arg:
            parts.append(''.join(current_arg))

        if inside_quotes is not None:
            raise ValueError("Error: Unmatched quote detected. Please ensure both quotes are closed.")
