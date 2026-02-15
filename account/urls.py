from django.urls import path
from .views import (
    signup_view, 
    signin_view, 
    logout_view, 
    verify_email, 
    profile_view, 
    change_password_view
)

app_name = "account"
urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password_view, name="password_change"),
    path("verify/<uuid:token>/", verify_email, name="verify_email"),
]