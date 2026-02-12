import csv
import re

EMAIL_REGEX = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

def get_valid_emails(file):
    emails = set()
    file.seek(0)

    decoded = file.read().decode('utf-8-sig').splitlines()
    reader = csv.DictReader(decoded)

    for row in reader:
        email = (
            row.get('email') or
            row.get('Email') or
            row.get('EMAIL') or
            ''
        ).strip().lower()

        if email and re.match(EMAIL_REGEX, email):
            emails.add(email)

    return list(emails)