from typing import Optional


class Validator:
    @staticmethod
    def validate_length(value: str, min_len: int = 3, max_len: int = 50) -> str:
        """
        Validates that the string length is within specified bounds.

        :param value: The string to validate.
        :param min_len: Minimum allowed length.
        :param max_len: Maximum allowed length.
        :return: Stripped string if valid.
        :raises ValueError: If the string length is out of bounds.
        """
        if not min_len <= len(value) <= max_len:
            raise ValueError(f"Value must be between {min_len} and {max_len} characters.")
        return value.strip()

    @staticmethod
    def validate_format(value: str) -> str:
        """
        Validates that the string contains only allowed characters.

        :param value: The string to validate.
        :return: Stripped string if valid.
        :raises ValueError: If the string contains disallowed characters.
        """
        if not all(c.isalnum() or c.isspace() or c in "-_" for c in value):
            raise ValueError("Value must contain only alphanumeric characters, spaces, hyphens, and underscores.")
        return value.strip()

    @staticmethod
    def validate_word_count(value: str, min_words: int = 1) -> str:
        """
        Validates that the string meets minimum word count requirements.

        :param value: The string to validate.
        :param min_words: Minimum number of words required.
        :return: Stripped string if valid.
        :raises ValueError: If word count is below the minimum.
        """
        if len(value.split()) < min_words:
            raise ValueError(f"Value should contain at least {min_words} word(s).")
        return value.strip()

    @staticmethod
    def validate_enum(value: Optional[str], allowed_values: list) -> str:
        """
        Validates that the value is one of the allowed options.

        :param value: The value to validate.
        :param allowed_values: A list of allowed values.
        :return: The value if valid.
        :raises ValueError: If the value is not one of the allowed values.
        """
        if value not in allowed_values:
            raise ValueError(f"Value must be one of the following: {', '.join(allowed_values)}.")
        return value
    
    @staticmethod
    def validate_name(name: str, min_len: int = 3, max_len: int = 50) -> str:
        """
        Validates name by checking length, format, and word count.

        :param name: The name to validate.
        :param min_len: Minimum allowed length.
        :param max_len: Maximum allowed length.
        :return: Stripped name if valid.
        """
        name = Validator.validate_length(name, min_len, max_len)
        name = Validator.validate_format(name)
        return Validator.validate_word_count(name)

    @staticmethod
    def validate_description(description: str, min_len: int = 10, min_words: int = 1) -> str:
        """
        Validates description by checking length, word count, and format.

        :param description: The description to validate.
        :param min_len: Minimum allowed length.
        :param min_words: Minimum number of words required.
        :return: Stripped description if valid.
        """
        description = Validator.validate_length(description, min_len)
        description = Validator.validate_format(description)
        description = Validator.validate_word_count(description, min_words)
        return description.strip()
