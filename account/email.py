from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator
from Eshop.settings import BASE_DIR, DEFAULT_APP_URL
from urllib3.util import parse_url
from os import path
from Eshop.settings import MY_APP_NAME
from .models import User

from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab
from django.utils import timezone


# if using celery uncomment the decorator passed to all class.


# @shared_task
class ActivationEmail(email.ActivationEmail):
    template_name = "account/ActivationEmail.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["app_name"] = MY_APP_NAME
        return context


@periodic_task(run_every=crontab(hour="*/12"))
def send_activation_email_periodically():
    # Get unverified users
    unverified_users = User.objects.filter(is_active=False)

    for user in unverified_users:
        # Check if activation email has not been sent within the last 12 hours
        if (
            not user.activation_email_reminder
            or (timezone.now() - user.activation_email_reminder).total_seconds()
            >= 43200
        ):
            # Send activation email
            activation_email = ActivationEmail()
            activation_email.send(user=user)

            # Update user's activation_email_sent_at timestamp
            user.activation_email_reminder = timezone.now()
            user.save()


# @shared_task
class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "account/ConfirmationEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["app_name"] = MY_APP_NAME
        return context


# @shared_task
class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "account/PasswordResetEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        url = parse_url(DEFAULT_APP_URL)
        context["app_name"] = MY_APP_NAME
        return context


# @shared_task
class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "account/PasswordChangedConfirmationEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["app_name"] = MY_APP_NAME
        return context
