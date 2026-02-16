from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ResetTokenGenerator(PasswordResetTokenGenerator):
    pass

password_reset_token = ResetTokenGenerator()