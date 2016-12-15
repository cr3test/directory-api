import datetime

from django.conf import settings

from company.stannp import stannp_client


def send_verification_letter(sender, instance, *args, **kwargs):
    is_disabled = not settings.FEATURE_VERIFICATION_LETTERS_ENABLED
    is_address_unknown = not instance.contact_details
    is_already_sent = instance.is_verification_letter_sent
    if is_disabled or is_already_sent or is_address_unknown:
        return

    recipient = instance.contact_details.copy()
    recipient['custom_fields'] = [
        ('full_name', recipient['postal_full_name']),
        ('company_name', instance.name),
        ('verification_code', instance.verification_code),
        ('date', datetime.date.today().strftime('%d/%m/%Y')),
        ('company', instance.name),
    ]

    stannp_client.send_letter(
        template=settings.STANNP_VERIFICATION_LETTER_TEMPLATE_ID,
        recipient=recipient
    )

    instance.is_verification_letter_sent = True
    instance.save()
