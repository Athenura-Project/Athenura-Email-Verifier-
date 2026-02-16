
from django.urls import path
from . import views

app_name = "email_verifier"

urlpatterns = [
    path("email-verifier/", views.index, name="index"),

    path(
        "download/csv/",
        views.download_verified_emails_csv,
        name="download_csv",
    ),

    path(
        "download/xlsx/",
        views.download_verified_emails_xlsx,
        name="download_xlsx",
    ),
]
