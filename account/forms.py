from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()


# ---------------- SIGNUP FORM ----------------

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["full_name", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


# ---------------- LOGIN FORM ----------------

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

# ----------------- Change FORM -------------

class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")

        if not self.user.check_password(current_password):
            raise forms.ValidationError("Current password is incorrect.")

        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")

            validate_password(new_password, self.user)

        return cleaned_data
    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_image",
            "phone_number",
            "date_of_birth",
            "bio"
        ]