import uuid

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_confirmation_email(sender, instance, created, *args, **kwargs):
    if not created or not instance.company_email:
        return

    if not instance.confirmation_code:
        instance.confirmation_code = str(uuid.uuid4())
        instance.save()

    subject = settings.CONFIRMATION_EMAIL_SUBJECT
    from_email = settings.CONFIRMATION_EMAIL_FROM
    url = settings.CONFIRMATION_URL_TEMPLATE % instance.confirmation_code

    text_body = render_to_string('confirmation_email.txt',
                                 {'confirmation_url': url})
    html_body = render_to_string('confirmation_email.html',
                                 {'confirmation_url': url})
    msg = EmailMultiAlternatives(subject, text_body, from_email,
                                 [instance.company_email])
    msg.attach_alternative(html_body, "text/html")
    msg.send()
