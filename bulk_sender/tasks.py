import requests
from datetime import date
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.db.models import F
from .models import Recipient, Campaign
from account.models import User


@shared_task(bind=True, max_retries=3)
def send_email(self, recipient_id):

    recipient = Recipient.objects.get(id=recipient_id)
    campaign = recipient.campaign
    user = campaign.user

    if user.last_sent_date != date.today():
        user.total_sent_today = 0
        user.last_sent_date = date.today()
        user.save()

    if user.total_sent_today >= user.daily_limit:
        recipient.status = "failed"
        recipient.save()
        Campaign.objects.filter(id=campaign.id).update(
            failed_count=F("failed_count") + 1
        )
        return "Daily limit exceeded"

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Bulk Sender",
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

        if response.status_code != 201:
            raise Exception(response.text)

        recipient.status = "sent"
        recipient.save()

        Campaign.objects.filter(id=campaign.id).update(
            sent_count=F("sent_count") + 1
        )

        User.objects.filter(id=user.id).update(
            total_sent_today=F("total_sent_today") + 1
        )

        return "Sent Successfully"

    except Exception as e:

        recipient.status = "failed"
        recipient.save()

        Campaign.objects.filter(id=campaign.id).update(
            failed_count=F("failed_count") + 1
        )

        raise self.retry(exc=e, countdown=60)
