from django.db import models
from account.models import User


class Campaign(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=255)
    message = models.TextField()

    total_emails = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Recipient(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    email = models.EmailField()

    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
        ),
        default='pending'
    )

    def __str__(self):
        return self.email
