def remove_duplicates(emails):
    unique = list(set(emails))
    removed = len(emails) - len(unique)
    return unique, removed
