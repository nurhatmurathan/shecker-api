from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config import settings


def send_verification_email(email: str, verification_code: str):
    subject = 'Email Verification'
    from_email = settings.EMAIL_HOST
    to_email = email

    html_content = render_to_string('verification_email.html', {'verification_code': verification_code})
    text_content = strip_tags(html_content)

    email_message = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
