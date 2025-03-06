from django.core.mail import send_mail

from config.settings import base


def send_email(subject, message, to_email):
    to_email = (
        to_email
        if isinstance(to_email, list)
        else [
            to_email,
        ]
    )

    send_mail(subject, message, base.EMAIL_HOST_USER, to_email)
