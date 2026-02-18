import re
from django.core.exceptions import ValidationError


def validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError(
            "Password must be at least 8 characters long."
        )

    if not re.search(r"[A-Za-z]", password):
        raise ValidationError(
            "Password must contain at least one letter."
        )

    if not re.search(r"\d", password):
        raise ValidationError(
            "Password must contain at least one number."
        )

    if not re.search(r"[^\w\s]", password):
        raise ValidationError(
            "Password must contain at least one special character."
        )

    return password