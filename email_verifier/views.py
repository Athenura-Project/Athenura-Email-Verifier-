
# # # from django.shortcuts import render

# # # # Create your views here.
# # # def index(request):
# # #     return render(request, 'email_verifier/index.html')


# from django.shortcuts import render
# from .email_cleaner import clean_emails
# from .duplicate_handler import remove_duplicates
# from .verifier import verify_emails

# def index(request):
#     context = {}

#     if request.method == "POST":
#         file = request.FILES['emails']
#         lines = file.read().decode(errors='ignore').splitlines()

#         cleaned = clean_emails(lines)
#         unique, _ = remove_duplicates(cleaned)
#         valid, invalid = verify_emails(unique)

#         context = {
#             "valid": valid,
#             "invalid": invalid,
#             "valid_count": len(valid),
#             "invalid_count": len(invalid),
#             "total": len(unique),
#         }

#     return render(request, "email_verifier/index.html", context)

# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
# import csv

# from .email_cleaner import clean_emails
# from .duplicate_handler import remove_duplicates
# from .verifier import verify_emails


# # Home page
# # def index(request):
# #     return render(request, 'email_verifier/index.html')

# # @csrf_exempt
# # def verify_email_file(request):
# #     if request.method == "POST" and request.FILES.get("emails"):
# #         uploaded_file = request.FILES["emails"]
# #         file_name = uploaded_file.name.lower()

# #         # Read emails
# #         if file_name.endswith(".csv"):
# #             df = pd.read_csv(uploaded_file)
# #             emails = df.iloc[:, 0].astype(str).tolist()

# #         elif file_name.endswith(".xlsx"):
# #             df = pd.read_excel(uploaded_file)
# #             emails = df.iloc[:, 0].astype(str).tolist()

# #         elif file_name.endswith(".txt"):
# #             emails = uploaded_file.read().decode("utf-8").splitlines()

# #         else:
# #             return render(request, "email_verifier/index.html", {
# #                 "error": "Unsupported file format"
# #             })

# #         cleaned = clean_emails(emails)
# #         unique, dup_count = remove_duplicates(cleaned)
# #         valid_emails, invalid_emails = verify_emails(unique)

# #         context = {
# #             "valid": valid_emails,
# #             "invalid": invalid_emails,
# #             "total": len(emails),
# #             "valid_count": len(valid_emails),
# #             "invalid_count": len(invalid_emails),
# #             "duplicates_removed": dup_count,
# #         }

# #         # store for download
# #         request.session["verified_emails"] = valid_emails

# #         return render(request, "email_verifier/index.html", context)


# def download_verified_emails(request):
#     """
#     Downloads verified emails as CSV
#     """

#     verified_emails = request.session.get("verified_emails", [])

#     response = HttpResponse(content_type="text/csv")
#     response["Content-Disposition"] = 'attachment; filename="verified_emails.csv"'

#     writer = csv.writer(response)
#     writer.writerow(["Email"])

#     for email in verified_emails:
#         writer.writerow([email])

#     return response


# def download_verified_emails_xlsx(request):

#     verified_emails = request.session.get("verified_emails", [])

#     if not verified_emails:
#         return JsonResponse({"error": "No verified emails to download"}, status=400)

#     df = pd.DataFrame(verified_emails, columns=["Email"])

#     response = HttpResponse(
#         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )
#     response["Content-Disposition"] = 'attachment; filename="verified_emails.xlsx"'

#     df.to_excel(response, index=False)

#     return response


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import csv
import pandas as pd

from .email_cleaner import clean_emails
from .duplicate_handler import remove_duplicates
from .verifier import verify_emails


def index(request):
    context = {}

    if request.method == "POST" and request.FILES.get("emails"):
        uploaded_file = request.FILES["emails"]
        file_name = uploaded_file.name.lower()

        # ---------- Read emails ----------
        try:
            if file_name.endswith(".txt"):
                emails = uploaded_file.read().decode("utf-8", errors="ignore").splitlines()

            elif file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
                emails = df.iloc[:, 0].astype(str).tolist()

            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
                emails = df.iloc[:, 0].astype(str).tolist()

            else:
                context["error"] = "Unsupported file format"
                return render(request, "email_verifier/index.html", context)

        except Exception as e:
            context["error"] = "File could not be processed"
            return render(request, "email_verifier/index.html", context)

        # ---------- Process emails ----------
        cleaned = clean_emails(emails)
        unique_emails, duplicate_count = remove_duplicates(cleaned)
        valid_emails, invalid_emails = verify_emails(unique_emails)

        # store valid emails for download
        request.session["verified_emails"] = valid_emails

        # ---------- Context ----------
        context = {
            "total": len(emails),
            "valid": valid_emails,
            "invalid": invalid_emails,
            "valid_count": len(valid_emails),
            "invalid_count": len(invalid_emails),
            "duplicates_removed": duplicate_count,
        }

    return render(request, "email_verifier/index.html", context)



def download_verified_emails_csv(request):
    verified_emails = request.session.get("verified_emails", [])

    if not verified_emails:
        return JsonResponse({"error": "No verified emails found"}, status=400)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="verified_emails.csv"'

    writer = csv.writer(response)
    writer.writerow(["Email"])

    for email in verified_emails:
        writer.writerow([email])

    return response


def download_verified_emails_xlsx(request):
    verified_emails = request.session.get("verified_emails", [])

    if not verified_emails:
        return JsonResponse({"error": "No verified emails found"}, status=400)

    df = pd.DataFrame(verified_emails, columns=["Email"])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="verified_emails.xlsx"'

    df.to_excel(response, index=False)

    return response
