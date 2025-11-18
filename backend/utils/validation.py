import re
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation failures."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


def require_fields(data: dict, required_fields: list[str]):
    """
    Ensure all required fields are present and non-empty.
    Raises ValidationError if something is missing.
    """
    missing = []
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing.append(field)

    if missing:
        raise ValidationError(
            "Missing required fields",
            {"missing_fields": missing}
        )


def parse_date(value: str, field_name: str, fmt: str = "%Y-%m-%d"):
    """
    Parse a date string (e.g., '2025-11-30') into a datetime.date.
    Raises ValidationError if format is wrong.
    """
    try:
        return datetime.strptime(value, fmt).date()
    except Exception:
        raise ValidationError(
            f"Invalid date format for '{field_name}', expected YYYY-MM-DD",
            {field_name: value}
        )


# ---------- email validation ----------

_email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str, field_name: str = "email"):
    """
    Simple email format validation: something@something.domain
    Raises ValidationError if invalid.
    """
    if not isinstance(email, str) or not _email_re.match(email):
        raise ValidationError(
            "Invalid email format",
            {field_name: email}
        )


# ---------- integer + range validation ----------

def ensure_int_in_range(value, field_name: str, min_value=None, max_value=None) -> int:
    """
    Convert value to int and enforce optional min/max.
    Raises ValidationError if conversion fails or range is violated.
    """
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise ValidationError(
            f"Invalid integer for '{field_name}'",
            {field_name: value}
        )

    if (min_value is not None) and (ivalue < min_value):
        raise ValidationError(
            f"Value for '{field_name}' must be >= {min_value}",
            {field_name: ivalue}
        )

    if (max_value is not None) and (ivalue > max_value):
        raise ValidationError(
            f"Value for '{field_name}' must be <= {max_value}",
            {field_name: ivalue}
        )

    return ivalue
