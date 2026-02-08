from .syntax_validator import is_valid_syntax
from .domain_validator import is_valid_domain

def verify_emails(emails):
    valid = []
    invalid = []

    for email in emails:
        if not is_valid_syntax(email):
            invalid.append({"email": email, "reason": "Invalid Format"})
        elif not is_valid_domain(email):
            invalid.append({"email": email, "reason": "Domain Not Found"})
        else:
            valid.append(email)

    return valid, invalid
