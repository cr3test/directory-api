import json
from unittest import mock, TestCase


VALID_REQUEST_DATA = {
    "aims": ['AIM1', 'AIM2'],
    "company_number": "01234567",
    "email": "test@example.com",
    "personal_name": "Test",
    "referrer": "email",
    "password": "hunter2"
}
VALID_REQUEST_DATA_JSON = json.dumps(VALID_REQUEST_DATA)


class MockBoto(TestCase):

    def setUp(self):
        self.boto_client_mock = mock.patch(
            'botocore.client.BaseClient._make_api_call'
        )
        self.boto_resource_mock = mock.patch(
            'boto3.resource'
        )

        self.boto_client_mock.start()
        self.boto_resource_mock.start()

    def tearDown(self):
        self.boto_client_mock.stop()
        self.boto_resource_mock.stop()
