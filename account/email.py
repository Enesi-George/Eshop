from celery import shared_task
from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator
from Eshop.settings import BASE_DIR, DEFAULT_APP_URL
from urllib3.util import parse_url
from os import path
from Eshop.settings import MY_APP_NAME


@shared_task
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


@shared_task
class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "account/ConfirmationEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["app_name"] = MY_APP_NAME
        return context


@shared_task
class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "account/PasswordResetEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        url = parse_url(DEFAULT_APP_URL)
        context["app_name"] = MY_APP_NAME
        return context


@shared_task
class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "account/PasswordChangedConfirmationEmail.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["app_name"] = MY_APP_NAME
        return context
