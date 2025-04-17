# accounts/utils.py

from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Token generator for password reset
account_activation_token = PasswordResetTokenGenerator()
