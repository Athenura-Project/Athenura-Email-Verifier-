from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.urls import reverse
from django.http import HttpResponse
from .forms import SignUpForm, SignInForm, ChangePasswordForm
from .models import User, EmailVerification
from .utils import send_verification_email, send_reset_email
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import password_reset_token
from django.core.exceptions import ValidationError
from .password_validators import validate_strong_password


# ---------------- SIGNUP VIEW ----------------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("email_verifier:index")

    if request.method == "POST":
        # 1. Capture the form data to preserve it if validation fails
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'terms': request.POST.get('terms', '')
        }

        # 2. Check Terms and Conditions explicitly
        if not request.POST.get('terms'):
            messages.error(request, "You must agree to the Terms and Conditions first.")
            return render(request, "account/signup.html", {"form_data": form_data})

        # 3. Check if Passwords match
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "account/signup.html", {"form_data": form_data})

        # 4. Check Password Strength using your custom validator
        try:
            validate_strong_password(password)
        except ValidationError as e:
            # Display the specific password error (e.g., "Must contain a number")
            for msg in e.messages:
                messages.error(request, msg)
            return render(request, "account/signup.html", {"form_data": form_data})

        # 5. Check if Email already exists
        if User.objects.filter(email=form_data['email']).exists():
            messages.error(request, "This email is already in use. Please sign in.")
            return render(request, "account/signup.html", {"form_data": form_data})

        # 6. Pass data to your SignUpForm for final model validation/saving
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = False
            user.is_verified = False
            
            # If your custom User model requires a full_name, save it here
            # user.full_name = form_data['full_name'] 
            
            user.save()

            # Create verification token
            verification = EmailVerification.objects.create(user=user)
            verification_link = request.build_absolute_uri(
                reverse("account:verify_email", args=[verification.token])
            )

            print("Verification:", verification_link)
            send_verification_email(user, verification_link)

            messages.success(
                request,
                "Account created successfully! Please check your email to verify your account."
            )
            return redirect("account:signin")

        else:
            # If the SignUpForm catches any other errors, display them
            for error in form.non_field_errors():
                messages.error(request, error)

            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            
            return render(request, "account/signup.html", {"form_data": form_data})

    else:
        # GET request: render empty form
        return render(request, "account/signup.html", {"form_data": {}})

# -------------------Profile View ----------------------

@login_required
def profile_view(request):

    profile = request.user.profile

    if request.method == "POST":

        # Update User Model
        request.user.full_name = request.POST.get("full_name")

        # Update Profile Model
        profile.phone_number = request.POST.get("phone_number")
        profile.date_of_birth = request.POST.get("date_of_birth")
        profile.bio = request.POST.get("bio")

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        request.user.save()
        profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("account:profile")
    return render(request, "account/profile.html")

# ---------------- VERIFY EMAIL ----------------

def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)

    if verification.is_used:
        return HttpResponse("Link already used.")

    if verification.is_expired():
        return HttpResponse("Verification link expired.")

    user = verification.user
    user.is_verified = True
    user.is_active = True
    user.save()

    verification.is_used = True
    verification.save()

    return redirect("account:signin")


# ---------------- LOGIN VIEW ----------------

def signin_view(request):
    if request.user.is_authenticated:
        return redirect("email_verifier:index")

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=email, password=password)

            if user is not None:

                if not user.is_verified:
                    messages.warning(request, "Please verify your email first.")
                    return redirect("account:signin")

                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("email_verifier:index")

        else:
            for error in form.non_field_errors():
                messages.error(request, error)

            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        form = SignInForm()

    return render(request, "account/signin.html", {"form": form})

# ---------------- Password Change --------------

@login_required
def change_password_view(request):

    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            request.user.set_password(new_password)
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, "Password updated successfully.")
            return redirect("account:change_password")

        else:
            # All form errors 
            for field in form.errors:
                for error in form.errors[field]:
                    messages.warning(request, error)

            return redirect("account:change_password")

    return render(request, "account/change_password.html")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            # Generate uid + token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)

            # Build reset link
            reset_link = request.build_absolute_uri(
                reverse("account:reset_password", kwargs={
                    "uidb64": uid,
                    "token": token
                })
            )
            print("reset link:", reset_link)

            # Send email using Brevo API
            send_reset_email(email, reset_link)

            messages.success(request, "Reset link sent to your email.")
            return redirect("account:signin")

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, "account/forgot_password.html")


def reset_password_view(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and password_reset_token.check_token(user, token):

        
        if request.method == "POST":
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, "account/reset_password.html")

            try:
                validate_strong_password(password1)
            except ValidationError as e:
                messages.error(request, e.messages[0])
                return render(request, "account/reset_password.html")

            user.set_password(password1)
            user.save()

            messages.success(request, "Password reset successful.")
            return redirect("account:signin")

        return render(request, "account/reset_password.html")
    
    else:
        messages.error(request, "Invalid or expired link.")
        return redirect("account:forgot_password")




# ---------------- LOGOUT ----------------

def logout_view(request):
    logout(request)
    return redirect("account:signin")