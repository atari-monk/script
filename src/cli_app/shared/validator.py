class Validator:
    @staticmethod
    def validate_name_length(name: str, min_len: int = 3, max_len: int = 50) -> str:
        """
        Validates that the name length is within specified bounds.

        :param name: The name to validate.
        :param min_len: Minimum allowed length (default is 3).
        :param max_len: Maximum allowed length (default is 50).
        :return: Stripped name if valid.
        :raises ValueError: If the name length is out of bounds.
        """
        if not min_len <= len(name) <= max_len:
            raise ValueError(f"Name must be between {min_len} and {max_len} characters.")
        return name

    @staticmethod
    def validate_name_format(name: str) -> str:
        """
        Validates that the name contains only allowed characters.

        :param name: The name to validate.
        :return: Stripped name if valid.
        :raises ValueError: If the name contains disallowed characters.
        """
        if not all(c.isalnum() or c.isspace() or c in "-_" for c in name):
            raise ValueError("Name must contain only alphanumeric characters, spaces, hyphens, and underscores.")
        return name

    @staticmethod
    def validate_name(name: str, min_len: int = 3, max_len: int = 50) -> str:
        """
        Combines length and format validation for a name.

        :param name: The name to validate.
        :param min_len: Minimum allowed length (default is 3).
        :param max_len: Maximum allowed length (default is 50).
        :return: Stripped name if valid.
        """
        name = Validator.validate_name_length(name, min_len, max_len)
        return Validator.validate_name_format(name)
