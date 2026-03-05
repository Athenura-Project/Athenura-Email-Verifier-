from django import forms
from .models import User, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from .password_validators import validate_strong_password

# ---------------- SIGNUP FORM ----------------

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_strong_password])
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    terms_accepted = forms.BooleanField(required=True, error_messages={"required": "You must accept the terms and conditions."})

    class Meta:
        model = User
        fields = ["full_name", "email", "password", "terms_accepted"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# ---------------- LOGIN FORM ----------------

class SignInForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    error_messages = {
        "invalid_login": "Invalid email or password.",
        "inactive": "This account is inactive.",
    }

# ----------------- Change FORM -------------

class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
        validators=[validate_strong_password]
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