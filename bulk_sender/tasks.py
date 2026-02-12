import requests
from celery import shared_task
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_email(self, recipient_email, subject, message):

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Bulk Sender",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {"email": recipient_email}
        ],
        "subject": subject,
        "htmlContent": message
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 201:
            raise Exception(response.text)

        return f"Sent to {recipient_email}"

    except Exception as e:
        raise self.retry(exc=e, countdown=60)