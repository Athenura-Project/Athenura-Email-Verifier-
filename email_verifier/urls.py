from django.urls import path
from . import views

app_name = 'email_verifier'
urlpatterns = [
    path('email/verify/', views.index, name='index'),   
]