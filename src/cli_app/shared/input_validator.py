import logging
logger = logging.getLogger(__name__)

class InputValidator:
    @staticmethod
    def validate_and_parse(field_value_pairs):
        update_data = {}
        for field_value in field_value_pairs:
            if "=" not in field_value:
                logger.error(f"Invalid format for '{field_value}', expected 'field=value'.")
                return None  # Returning None to indicate invalid input

            field, value = field_value.split("=", 1)
            update_data[field.lower()] = value.strip()

        return update_data
