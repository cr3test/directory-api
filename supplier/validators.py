from rest_framework.serializers import ValidationError

from user.models import User as Supplier


EMAIL_NOT_UNIQUE_MESSAGE = 'This email address has already been registered.'
MOBILE_NOT_UNIQUE_MESSAGE = 'This phone number has already been registered.'


def email_unique(email):
    if Supplier.objects.filter(company_email=email).exists():
        raise ValidationError(EMAIL_NOT_UNIQUE_MESSAGE)


def mobile_number_unique(mobile_number):
    if Supplier.objects.filter(mobile_number=mobile_number).exists():
        raise ValidationError(MOBILE_NOT_UNIQUE_MESSAGE)
