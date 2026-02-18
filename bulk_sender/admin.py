from django.contrib import admin
from .models import Campaign, Recipient


class RecipientInline(admin.TabularInline):
    model = Recipient
    extra = 0
    readonly_fields = ("email", "status")
    can_delete = False


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "subject",
        "total_emails",
        "sent_count",
        "failed_count",
        "success_rate",  
        "created_at",
    )

    list_filter = ("created_at", "user")
    search_fields = ("subject", "user__email")
    readonly_fields = ("total_emails", "sent_count", "failed_count")

    inlines = [RecipientInline]

    def success_rate(self, obj):
        if obj.total_emails == 0:
            return "0%"
        return f"{(obj.sent_count / obj.total_emails) * 100:.2f}%"

    success_rate.short_description = "Success Rate"


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):

    list_display = ("id", "campaign", "email", "status")
    list_filter = ("status", "campaign")
    search_fields = ("email",)