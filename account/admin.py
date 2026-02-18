from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerification, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    ordering = ['email']

    list_display = (
        'email',
        'full_name',
        'is_verified',
        'is_active',
        'daily_limit',
        'total_sent_today',
    )

    search_fields = ('email', 'full_name')

    list_filter = ('is_verified', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_verified',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Email Stats', {
            'fields': ('daily_limit', 'total_sent_today')
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'expires_at', 'is_used')
    search_fields = ('user__email',)

admin.site.register(Profile)