from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse
from .forms import SignUpForm, SignInForm
from .models import EmailVerification
from .utils import send_verification_email
from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# ---------------- SIGNUP VIEW ----------------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("email_verifier:index")
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_active = False
            user.is_verified = False
            user.save()

            # create token
            verification = EmailVerification.objects.create(user=user)

            verification_link = request.build_absolute_uri(
                reverse("account:verify_email", args=[verification.token])
            )

            # Send email
            send_verification_email(user, verification_link)

            print("Verification link:", verification_link)

            return render(request, "account/verification_sent.html")

    else:
        form = SignUpForm()

    return render(request, "account/signup.html", {"form": form})

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
                    return HttpResponse("Please verify your email first.")

                login(request, user)
                return redirect("email_verifier:index")

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

            # IMPORTANT: Keep user logged in
            update_session_auth_hash(request, request.user)

            messages.success(request, "Password updated successfully.")
            return redirect("account:password_change")

    else:
        form = ChangePasswordForm(request.user)

    return render(request, "account/change_password.html", {"form": form})

# ---------------- LOGOUT ----------------

def logout_view(request):
    logout(request)
    return redirect("account:signin")