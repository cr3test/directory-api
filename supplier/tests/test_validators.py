import pytest

from rest_framework.serializers import ValidationError

from supplier import validators
from supplier.tests import VALID_REQUEST_DATA
from user.models import User as Supplier


@pytest.mark.django_db
def test_email_unique_rejects_existing(client):
    expected_message = validators.EMAIL_NOT_UNIQUE_MESSAGE
    Supplier.objects.create(**VALID_REQUEST_DATA)
    with pytest.raises(ValidationError, message=expected_message):
        validators.email_unique(VALID_REQUEST_DATA['company_email'])


@pytest.mark.django_db
def test_email_unique_accepts_new(client):
    assert validators.email_unique('test@example.com') is None
