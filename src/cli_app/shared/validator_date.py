from datetime import date, datetime

class ValidatorDate:
    @staticmethod
    def validate_date(value: str, date_format: str = "%Y-%m-%d") -> date:
        """
        Validates if the provided date string matches the given format and returns it as a date object.

        :param value: The date string to validate.
        :param date_format: The expected format of the date (default is "%Y-%m-%d").
        :return: The validated date as a datetime.date object.
        :raises ValueError: If the date format is invalid.
        """
        try:
            date_obj = datetime.strptime(value, date_format).date()
        except ValueError:
            raise ValueError(f"Date must be in the format {date_format}.")
        return date_obj

    @staticmethod
    def validate_relation(start_date: date, end_date: date):
        """
        Validates that the end date is after the start date.
        
        :param start_date: The start date to validate.
        :param end_date: The end date to validate.
        :raises ValueError: If the end date is before the start date.
        """
        if end_date < start_date:
            raise ValueError(f"End date must be after {start_date.isoformat()}.")
