import json
import base64
from unittest import TestCase
from unittest.mock import patch

from django.core.urlresolvers import reverse

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from user.models import User as Supplier
from supplier.tests import (
    VALID_REQUEST_DATA,
    MockInvalidSerializer,
    MockValidSerializer
)


class SupplierViewsTests(TestCase):

    def setUp(self):
        self.signature_permission_mock = patch(
            'signature.permissions.SignaturePermission.has_permission'
        )

        self.signature_permission_mock.start()

    def tearDown(self):
        self.signature_permission_mock.stop()

    @pytest.mark.django_db
    def test_supplier_retrieve_view(self):
        client = APIClient()
        supplier = Supplier.objects.create(**VALID_REQUEST_DATA)

        response = client.get(
            reverse('supplier', kwargs={'sso_id': supplier.sso_id})
        )

        expected = {'sso_id': str(supplier.sso_id), 'company': None}
        expected.update(VALID_REQUEST_DATA)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected

    @pytest.mark.django_db
    def test_supplier_update_view_with_put(self):
        client = APIClient()
        supplier = Supplier.objects.create(
            sso_id=1,
            company_email='harry.potter@hogwarts.com')

        response = client.put(
            reverse('supplier', kwargs={'sso_id': supplier.sso_id}),
            VALID_REQUEST_DATA, format='json')

        expected = {'sso_id': str(supplier.sso_id), 'company': None}
        expected.update(VALID_REQUEST_DATA)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected

    @pytest.mark.django_db
    def test_supplier_update_view_with_patch(self):
        client = APIClient()
        supplier = Supplier.objects.create(
            sso_id=1, company_email='harry.potter@hogwarts.com'
        )

        response = client.patch(
            reverse('supplier', kwargs={'sso_id': supplier.sso_id}),
            VALID_REQUEST_DATA, format='json')

        expected = {'sso_id': str(supplier.sso_id), 'company': None}
        expected.update(VALID_REQUEST_DATA)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected

    @pytest.mark.django_db
    def test_confirm_company_email_view_invalid_confirmation_code(self):
        supplier = Supplier.objects.create(
            sso_id=1,
            company_email='gargoyle@example.com',
            company_email_confirmation_code='123456789'
        )

        client = APIClient()
        response = client.post(
            '/enrolment/confirm/',
            data={'confirmation_code': 12345678}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response_data = json.loads(response.data)
        assert response_data['status_code'] == status.HTTP_400_BAD_REQUEST
        assert response_data['detail'] == (
            'Invalid company email confirmation code'
        )

        assert Supplier.objects.get(
            sso_id=supplier.sso_id
        ).company_email_confirmed is False

    @pytest.mark.django_db
    def test_confirm_company_email_view_valid_confirmation_code(self):
        company_email_confirmation_code = '123456789'

        supplier = Supplier.objects.create(
            sso_id=1,
            company_email='gargoyle@example.com',
            company_email_confirmation_code=company_email_confirmation_code
        )

        client = APIClient()
        response = client.post(
            '/enrolment/confirm/',
            data={'confirmation_code': company_email_confirmation_code}
        )
        assert response.status_code == status.HTTP_200_OK

        response_data = json.loads(response.data)
        assert response_data['status_code'] == status.HTTP_200_OK
        assert response_data['detail'] == "Company email confirmed"

        assert Supplier.objects.get(
            sso_id=supplier.sso_id
        ).company_email_confirmed is True

    @pytest.mark.django_db
    @patch('supplier.views.SupplierEmailValidatorAPIView.get_serializer')
    def test_supplier_email_validator_rejects_invalid_serializer(
            self, mock_get_serializer):

        client = APIClient()
        serializer = MockInvalidSerializer(data={})
        mock_get_serializer.return_value = serializer
        response = client.get(reverse('validate-email-address'), {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == serializer.errors

    @pytest.mark.django_db
    @patch('supplier.views.SupplierEmailValidatorAPIView.get_serializer')
    def test_supplier_email_validator_accepts_valid_serializer(
            self, mock_get_serializer):

        client = APIClient()
        mock_get_serializer.return_value = MockValidSerializer(data={})
        response = client.get(reverse('validate-email-address'), {})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_gecko_num_registered_supplier_view_returns_correct_json():
    client = APIClient()
    Supplier.objects.create(**VALID_REQUEST_DATA)
    # Use basic auth with user=gecko and pass=X
    encoded_creds = base64.b64encode(
        'gecko:X'.encode('ascii')).decode("ascii")
    client.credentials(HTTP_AUTHORIZATION='Basic ' + encoded_creds)

    response = client.get(reverse('gecko-total-registered-suppliers'))

    expected = {
        "item": [
            {
              "value": 1,
              "text": "Total registered suppliers"
            }
          ]
    }
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


@pytest.mark.django_db
def test_gecko_num_registered_supplier_view_requires_auth():
    client = APIClient()

    response = client.get(reverse('gecko-total-registered-suppliers'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_gecko_num_registered_supplier_view_rejects_incorrect_creds():
    client = APIClient()
    # correct creds are gecko:X
    encoded_creds = base64.b64encode(
        'user:pass'.encode('ascii')).decode("ascii")
    client.credentials(HTTP_AUTHORIZATION='Basic ' + encoded_creds)

    response = client.get(reverse('gecko-total-registered-suppliers'))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
