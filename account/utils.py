import requests
from django.conf import settings


def send_verification_email(user, verification_link):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": settings.SENDER_NAME,
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {"email": user.email}
        ],
        "subject": "Verify Your Email",
        "htmlContent": f"""
        <h2>Dear {user.full_name}</h2>
        <p>Click below to verify your account:</p>
        <a href="{verification_link}" 
           style="padding:10px 20px;background:#4f46e5;color:white;text-decoration:none;border-radius:5px;">
           Verify Email
        </a>
        <p>This link will expire in 24 hours.</p>
        """
    }

    response = requests.post(url, json=payload, headers=headers)

    # print("Brevo response:", response.status_code, response.text)


def send_reset_email(recipient_email, reset_link):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": settings.SENDER_NAME,
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {"email": recipient_email}
        ],
        "subject": "Reset Your Password",
        "htmlContent": f"""
            <h2>Password Reset</h2>
            <p>Click the button below to reset your password:</p>
            <a href="{reset_link}" 
               style="padding:10px 20px;background:#4f46e5;color:white;text-decoration:none;border-radius:5px;">
               Reset Password
            </a>
        """
    }

    requests.post(url, json=payload, headers=headers)