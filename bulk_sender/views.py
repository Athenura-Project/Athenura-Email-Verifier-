from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from celery import group

from .forms import EmailForm
from .tasks import send_email
from .utils import get_valid_emails
from .models import Campaign, Recipient


@login_required
def index(request):

    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data["file"]
            subject = form.cleaned_data["subject"]
            message_body = form.cleaned_data["message"]

            emails = get_valid_emails(file)

            if not emails:
                messages.warning(request, "No valid emails found.")
                return redirect("bulk_sender:index")

            campaign = Campaign.objects.create(
                user=request.user,
                subject=subject,
                message=message_body,
                total_emails=len(emails)
            )

            recipients = [
                Recipient(campaign=campaign, email=email)
                for email in emails
            ]

            Recipient.objects.bulk_create(recipients)

            recipients = Recipient.objects.filter(campaign=campaign)

            job = group(
                send_email.s(recipient.id)
                for recipient in recipients
            )

            job.apply_async()

            messages.success(request, "Emails are being sent.")
            return redirect("bulk_sender:index")

    else:
        form = EmailForm()

    return render(request, "bulk_sender/index.html", {"form": form})