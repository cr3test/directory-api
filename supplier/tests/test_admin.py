from unittest import TestCase

from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import pytest

from freezegun import freeze_time

from user.models import User as Supplier
from supplier.tests import VALID_REQUEST_DATA as SUPPLIER_DATA
from company.models import Company
from company.tests import VALID_REQUEST_DATA as COMPANY_DATA


headers = (
    'company__date_of_creation,company__description,company__employees,'
    'company__export_status,company__is_published,company__keywords,'
    'company__logo,company__name,company__number,company__revenue,'
    'company__sectors,company__website,company_email,'
    'company_email_confirmed,company_id,date_joined,is_active,'
    'mobile_number,name,sso_id'
)


@pytest.mark.django_db
class DownloadCSVTestCase(TestCase):

    def setUp(self):
        superuser = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='test'
        )
        self.client = Client()
        self.client.force_login(superuser)

        self.freezer = freeze_time("2012-01-14 12:00:00")
        self.freezer.start()

    def tearDown(self):
        self.freezer.stop()

    def test_download_csv(self):
        company = Company.objects.create(**COMPANY_DATA)
        supplier = Supplier.objects.create(company=company, **SUPPLIER_DATA)

        data = {
            'action': 'download_csv',
            '_selected_action': Supplier.objects.all().values_list(
                'pk', flat=True
            )
        }
        response = self.client.post(
            reverse('admin:user_user_changelist'),
            data,
            follow=True
        )

        row_one = (
            '2010-10-10,Company description,,YES,False,,,Test Company,'
            '11234567,100000.00,,http://example.com,gargoyle@example.com,'
            'False,{pk},2017-03-21 13:12:00+00:00,True,,,1'
        ).format(pk=supplier.company.pk)

        actual = str(response.content, 'utf-8').split('\r\n')

        assert actual[0] == headers
        assert actual[1] == row_one

    def test_download_csv_multiple_suppliers(self):
        company1 = Company.objects.create(**COMPANY_DATA)
        company2 = Company.objects.create(number="01234568")
        supplier_data2 = {
            "sso_id": 2,
            "company_email": "2@example.com"
        }
        supplier_data3 = {
            "sso_id": 3,
            "company_email": "3@example.com",
            "mobile_number": "07505605134"
        }

        supplier_one = Supplier.objects.create(
            company=company1, **SUPPLIER_DATA
        )
        supplier_two = Supplier.objects.create(
            company=company2, **supplier_data2
        )
        supplier_three = Supplier.objects.create(
            company=company2, **supplier_data3
        )

        data = {
            'action': 'download_csv',
            '_selected_action': Supplier.objects.all().values_list(
                'pk', flat=True
            )
        }
        response = self.client.post(
            reverse('admin:user_user_changelist'),
            data,
            follow=True
        )

        row_one = (
            ',,,,False,,,,01234568,,,,3@example.com,False,{pk},'
            '2012-01-14 12:00:00+00:00,True,07505605134,,3'
        ).format(pk=supplier_three.company.pk)
        row_two = (
            ',,,,False,,,,01234568,,,,2@example.com,False,{pk},'
            '2012-01-14 12:00:00+00:00,True,,,2'
        ).format(pk=supplier_two.company.pk)
        row_three = (
            '2010-10-10,Company description,,YES,False,,,Test Company,'
            '11234567,100000.00,,http://example.com,gargoyle@example.com,'
            'False,{pk},2017-03-21 13:12:00+00:00,True,,,1'
        ).format(pk=supplier_one.company.pk)

        actual = str(response.content, 'utf-8').split('\r\n')

        assert actual[0] == headers
        assert actual[1] == row_one
        assert actual[2] == row_two
        assert actual[3] == row_three
