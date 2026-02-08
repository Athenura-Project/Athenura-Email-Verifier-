import re

EMAIL_REGEX = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'

def is_valid_syntax(email):
    return re.match(EMAIL_REGEX, email) is not None
