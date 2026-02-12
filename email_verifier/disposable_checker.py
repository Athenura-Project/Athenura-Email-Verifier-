import os

BASE_DIR = os.path.dirname(__file__)
BLOCKLIST_FILE = os.path.join(BASE_DIR, "disposable_email_blocklist.conf")

# Load once at startup
def load_disposable_domains():
    try:
        with open(BLOCKLIST_FILE, "r", encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()

DISPOSABLE_DOMAINS = load_disposable_domains()

def is_disposable_domain(domain):
    return domain.lower() in DISPOSABLE_DOMAINS
