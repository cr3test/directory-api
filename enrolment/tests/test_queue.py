from unittest import mock

import pytest

import enrolment.queue
import enrolment.models
from enrolment.tests import (
    MockBoto, VALID_REQUEST_DATA, VALID_REQUEST_DATA_JSON
)


class TestQueueWorker(MockBoto):

    def test_is_valid_enrolment(self):
        assert not enrolment.queue.Worker.is_valid_enrolment(
            'not valid'
        )
        assert enrolment.queue.Worker.is_valid_enrolment(
            VALID_REQUEST_DATA_JSON
        )

    @pytest.mark.django_db
    def test_process_message(self):
        """ Test processing a message creates a new .models.Enrolment object
        """
        worker = enrolment.queue.Worker()
        worker.process_message(
            mock.Mock(message_id='1', body=VALID_REQUEST_DATA_JSON)
        )
        instance = enrolment.models.Enrolment.objects.last()
        assert instance.aims == VALID_REQUEST_DATA['aims']
        assert instance.company_number == VALID_REQUEST_DATA['company_number']
        assert instance.email == VALID_REQUEST_DATA['email']
        assert instance.personal_name == VALID_REQUEST_DATA['personal_name']
