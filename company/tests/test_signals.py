import datetime
from unittest import mock

import pytest

from company.models import Company
from company.tests import VALID_REQUEST_DATA


@pytest.mark.django_db
def test_sends_verification_letter_post_save(settings, ):
    settings.FEATURE_VERIFICATION_LETTERS_ENABLED = True

    with mock.patch('requests.post') as requests_mock:
        company = Company.objects.create(**VALID_REQUEST_DATA)

    company.refresh_from_db()
    assert company.verification_code

    requests_mock.assert_called_once_with(
        'https://dash.stannp.com/api/v1/letters/create',
        auth=('debug', ''),
        data={
            'recipient[date]': datetime.date.today().strftime('%d/%m/%Y'),
            'recipient[address1]': 'test_address_line_1',
            'recipient[postcode]': 'test_postal_code',
            'recipient[company_name]': 'Test Company',
            'recipient[country]': 'test_country',
            'recipient[verification_code]': company.verification_code,
            'test': True, 'recipient[title]': '',
            'recipient[address2]': 'test_address_line_2',
            'template': 'debug',
            'recipient[city]': 'test_locality'
        }
    )


@pytest.mark.django_db
def test_does_not_send_verification_letter_on_update(settings):
    settings.FEATURE_VERIFICATION_LETTERS_ENABLED = True

    with mock.patch('requests.post') as requests_mock:
        company = Company.objects.create(**VALID_REQUEST_DATA)
        company.name = "Changed"
        company.save()

    requests_mock.assert_called_once_with(
        'https://dash.stannp.com/api/v1/letters/create',
        auth=('debug', ''),
        data={
            'recipient[date]': datetime.date.today().strftime('%d/%m/%Y'),
            'recipient[address1]': 'test_address_line_1',
            'recipient[postcode]': 'test_postal_code',
            'recipient[company_name]': 'Test Company',
            'recipient[country]': 'test_country',
            'recipient[verification_code]': company.verification_code,
            'test': True, 'recipient[title]': '',
            'recipient[address2]': 'test_address_line_2',
            'template': 'debug',
            'recipient[city]': 'test_locality'
        },
    )


@pytest.mark.django_db
def test_does_not_overwrite_verification_code_if_already_set(settings):
    settings.FEATURE_VERIFICATION_LETTERS_ENABLED = True

    with mock.patch('requests.post'):
        company = Company.objects.create(
            verification_code='test', **VALID_REQUEST_DATA
        )

    company.refresh_from_db()
    assert company.verification_code == 'test'


@pytest.mark.django_db
@mock.patch('company.stannp.stannp_client')
def test_does_not_send_if_letter_already_sent(mock_stannp_client, settings):
    settings.FEATURE_VERIFICATION_LETTERS_ENABLED = True
    Company.objects.create(
        is_verification_letter_sent=True,
        verification_code='test',
        **VALID_REQUEST_DATA
    )

    mock_stannp_client.assert_not_called()


@pytest.mark.django_db
@mock.patch('company.stannp.stannp_client')
def test_marks_letter_as_sent(mock_stannp_client, settings):
    settings.FEATURE_VERIFICATION_LETTERS_ENABLED = True
    company = Company.objects.create(
        verification_code='test',
        **VALID_REQUEST_DATA
    )

    company.refresh_from_db()
    assert company.is_verification_letter_sent is True
