import requests
from celery import shared_task
from django.conf import settings
from django.db.models import F
from .models import Recipient, Campaign
from account.models import User


@shared_task(bind=True, max_retries=3)
def send_email(self, recipient_id):

    recipient = Recipient.objects.get(id=recipient_id)
    campaign = recipient.campaign
    user = campaign.user

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": settings.SENDER_NAME,
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [
            {"email": recipient.email}
        ],
        "subject": campaign.subject,
        "htmlContent": campaign.message
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code not in [200, 201, 202]:
            raise Exception(response.text)

        recipient.status = "sent"
        recipient.save()

        Campaign.objects.filter(id=campaign.id).update(
            sent_count=F("sent_count") + 1
        )

        User.objects.filter(id=user.id).update(
            total_sent_emails=F("total_sent_emails") + 1
        )

        return "Sent Successfully"

    except Exception as e:

        recipient.status = "failed"
        recipient.save()

        Campaign.objects.filter(id=campaign.id).update(
            failed_count=F("failed_count") + 1
        )

        raise self.retry(exc=e, countdown=60)