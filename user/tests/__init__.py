import json

from rest_framework import serializers


VALID_REQUEST_DATA = {
    "sso_id": 1,
    "company_email": "gargoyle@example.com",
    "date_joined": "2017-03-21T13:12:00Z",
    "mobile_number": "07505605132",
}
VALID_REQUEST_DATA_JSON = json.dumps(VALID_REQUEST_DATA)


class MockInvalidSerializer(serializers.Serializer):
    company_email = serializers.CharField()


class MockValidSerializer(serializers.Serializer):
    company_email = serializers.CharField(required=False)
