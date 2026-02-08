def clean_emails(emails):
    cleaned = []
    for email in emails:
        if email:
            email = email.strip().lower()
            if email:
                cleaned.append(email)
    return cleaned
