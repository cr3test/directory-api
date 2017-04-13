import http
from unittest.mock import Mock, patch

import pytest

from django.core.signing import Signer
from django.core.urlresolvers import reverse

from notifications import models


@pytest.mark.django_db
@patch('signature.permissions.SignatureCheckPermission.has_permission', Mock)
def test_create_anonymous_unsubscribe_create_bad_signature(client):
    url = reverse('anonymous-unsubscribe')
    response = client.post(url, {'email': 'test@example.com'})

    assert response.status_code == http.client.BAD_REQUEST


@pytest.mark.django_db
@patch('signature.permissions.SignatureCheckPermission.has_permission', Mock)
def test_create_anonymous_unsubscribe_create_good_signature(client):
    url = reverse('anonymous-unsubscribe')
    email = 'test@example.com'
    response = client.post(url, {'email': Signer().sign(email)})

    assert response.status_code == http.client.CREATED
    assert models.AnonymousUnsubscribe.objects.filter(email=email).exists()


@pytest.mark.django_db
@patch('signature.permissions.SignatureCheckPermission.has_permission', Mock)
def test_create_anonymous_unsubscribe_multiple_times(client):
    url = reverse('anonymous-unsubscribe')
    email = 'test@example.com'
    client.post(url, {'email': Signer().sign(email)})

    response = client.post(url, {'email': Signer().sign(email)})

    assert response.status_code == http.client.OK
