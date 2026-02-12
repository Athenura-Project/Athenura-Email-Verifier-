import dns.resolver

def has_mx_record(domain):
    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except:
        return False
