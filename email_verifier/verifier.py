from .disposable_checker import is_disposable_domain
from .domain_validator import has_mx_record
from .syntax_validator import is_valid_syntax

def verify_emails(emails):
    valid = []
    invalid = []

    for email in emails:
        if not is_valid_syntax(email):
            invalid.append({"email": email, "reason": "Invalid Format"})
            continue

        domain = email.split("@")[1]

        if is_disposable_domain(domain):
            invalid.append({"email": email, "reason": "Disposable Email"})
            continue

        if not has_mx_record(domain):
            invalid.append({"email": email, "reason": "No MX Record"})
            continue

        valid.append(email)

    return valid, invalid
