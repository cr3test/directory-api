from unittest import mock

import pytest
from rest_framework import status

from rest_framework.test import APIClient

from django.test import RequestFactory, TestCase

from company.models import Company
from enrolment.tests import VALID_REQUEST_DATA
from user.models import User as Supplier


class CompanyViewsTests(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.signature_permission_mock = mock.patch(
            'api.signature.SignatureCheckPermission.has_permission'
        )

        self.signature_permission_mock.start()

    def tearDown(self):
        self.signature_permission_mock.stop()

    @pytest.mark.django_db
    @mock.patch('boto3.resource')
    def test_enrolment_viewset_create(self, boto_mock):
        client = APIClient()
        response = client.post(
            '/enrolment/', VALID_REQUEST_DATA, format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Company.objects.filter(
            number=VALID_REQUEST_DATA['company_number']
        ).exists()
        assert Supplier.objects.filter(
            sso_id=VALID_REQUEST_DATA['sso_id'],
        ).exists()

    @pytest.mark.django_db
    def test_enrolment_viewset_create_invalid_data(self):
        client = APIClient()
        invalid_data = VALID_REQUEST_DATA.copy()
        del invalid_data['company_number']
        response = client.post(
            '/enrolment/', invalid_data, format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == ['Missing key: "\'company_number\'"']
