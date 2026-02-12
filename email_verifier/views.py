from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pandas as pd
import csv

from .email_cleaner import clean_emails
from .duplicate_handler import remove_duplicates
from .verifier import verify_emails


# Home page
def index(request):
    return render(request, 'email_verifier/index.html')


def verify_email_file(request):
    """
    Handles:
    - File upload (.csv, .xlsx, .txt)
    - Email verification
    - Report generation
    - Download of verified emails
    """

    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        file_name = uploaded_file.name

        # Read emails from file
        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            emails = df.iloc[:, 0].astype(str).tolist()

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            emails = df.iloc[:, 0].astype(str).tolist()

        elif file_name.endswith(".txt"):
            emails = uploaded_file.read().decode("utf-8").splitlines()

        else:
            return JsonResponse({"error": "Unsupported file format"}, status=400)

        # Clean emails
        cleaned = clean_emails(emails)

        # Remove duplicates
        unique, dup_count = remove_duplicates(cleaned)

        # Verify emails
        valid_emails, invalid_emails = verify_emails(unique)

        # Verification report
        report = {
            "total_emails": len(emails),
            "duplicates_removed": dup_count,
            "valid_count": len(valid_emails),
            "invalid_count": len(invalid_emails),
        }

        # Store verified emails in session (for download)
        request.session["verified_emails"] = valid_emails

        return JsonResponse({
            "report": report,
            "valid_emails": valid_emails,
            "invalid_emails": invalid_emails
        })

    return JsonResponse({"message": "Upload a file to verify emails"})


def download_verified_emails(request):
    """
    Downloads verified emails as CSV
    """

    verified_emails = request.session.get("verified_emails", [])

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="verified_emails.csv"'

    writer = csv.writer(response)
    writer.writerow(["Email"])

    for email in verified_emails:
        writer.writerow([email])

    return response


def download_verified_emails_xlsx(request):
    """
    Downloads verified emails as XLSX
    """

    verified_emails = request.session.get("verified_emails", [])

    if not verified_emails:
        return JsonResponse({"error": "No verified emails to download"}, status=400)

    df = pd.DataFrame(verified_emails, columns=["Email"])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="verified_emails.xlsx"'

    df.to_excel(response, index=False)

    return response
