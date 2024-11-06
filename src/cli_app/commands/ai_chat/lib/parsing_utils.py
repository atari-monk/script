class ParsingUtils:
    @staticmethod
    def validate_and_append_extension(file_name: str, extension: str = '.json') -> str:
        """Validates the file name and ensures it has the correct extension."""
        if not file_name.endswith(extension):
            file_name += extension
        return file_name

    @staticmethod
    def validate_args(args, required_count: int, param_names: list):
        """Validates the number of arguments passed and ensures they're not empty."""
        if len(args) != required_count:
            print(f"Error: Please provide {required_count} arguments: {', '.join(param_names)}.")
            return False
        
        for i, arg in enumerate(args):
            if not arg:
                print(f"Error: '{param_names[i]}' cannot be empty.")
                return False
        
        return True
