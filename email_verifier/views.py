# from django.shortcuts import render

# # Create your views here.
# def index(request):
#     return render(request, 'email_verifier/index.html')


from django.shortcuts import render
from .email_cleaner import clean_emails
from .duplicate_handler import remove_duplicates
from .verifier import verify_emails

def index(request):
    context = {}

    if request.method == "POST":
        file = request.FILES['emails']
        lines = file.read().decode(errors='ignore').splitlines()

        cleaned = clean_emails(lines)
        unique, _ = remove_duplicates(cleaned)
        valid, invalid = verify_emails(unique)

        context = {
            "valid": valid,
            "invalid": invalid,
            "valid_count": len(valid),
            "invalid_count": len(invalid),
            "total": len(unique),
        }

    return render(request, "email_verifier/index.html", context)
