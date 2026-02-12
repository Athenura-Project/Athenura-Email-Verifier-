from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("verify/", views.verify_email_file, name="verify_email_file"),
    path("download/csv/", views.download_verified_emails, name="download_csv"),
    path("download/xlsx/", views.download_verified_emails_xlsx, name="download_xlsx"),
]
