# from django.urls import path
# from . import views 
# app_name = 'email_verifier'
# urlpatterns = [
#     path('', views.index, name='index'),   
#     path('', views.download_verified_emails, name="download_csv"),
#     path('', views.download_verified_emails_xlsx, name="download_xlsx"),
# ]

from django.urls import path
from . import views

app_name = "email_verifier"

urlpatterns = [
    path("", views.index, name="index"),

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
