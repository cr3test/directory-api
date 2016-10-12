from unittest import mock

import pytest

from rest_framework.test import APIClient
from rest_framework import status

from enrollment.models import Enrollment
from enrollment.tests import VALID_REQUEST_DATA


@pytest.mark.django_db
def test_enrollment_viewset_create():
    with mock.patch('boto3.resource') as boto_mock:
        client = APIClient()
        response = client.post(
            '/enrollment/', VALID_REQUEST_DATA, format='json'
        )

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert not Enrollment.objects.all().exists()
    assert boto_mock.called
