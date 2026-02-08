import dns.resolver

def is_valid_domain(email):
    try:
        domain = email.split("@")[1]
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False
