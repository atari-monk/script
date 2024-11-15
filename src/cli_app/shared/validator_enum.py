from enum import Enum
from typing import List

class ValidatorEnum:
    @staticmethod
    def validate_enum_by_list(value: str, allowed_values: List[str]) -> str:
        """
        Validates that the value is one of the allowed options provided as a list.

        :param value: The value to validate.
        :param allowed_values: A list of allowed values.
        :return: The value if valid.
        :raises ValueError: If the value is not one of the allowed values.
        """
        if value not in allowed_values:
            raise ValueError(f"Value must be one of the following: {', '.join(allowed_values)}.")
        return value

    @staticmethod
    def validate_enum_by_class(value: str, enum_class: Enum) -> str:
        """
        Validates that the value is one of the allowed options in the Enum class.

        :param value: The value to validate.
        :param enum_class: The Enum class containing allowed values.
        :return: The value if valid.
        :raises ValueError: If the value is not in the Enum.
        """
        allowed_values = [e.value for e in enum_class]
        if value not in allowed_values:
            raise ValueError(f"Value must be one of the following: {', '.join(allowed_values)}.")
        return value
