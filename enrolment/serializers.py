from rest_framework import serializers

from django.db import transaction

from enrolment import models
from company.serializers import CompanySerializer
from supplier.serializers import SupplierSerializer


class EnrolmentSerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    data = serializers.JSONField(binary=True)

    class Meta(object):
        model = models.Enrolment
        fields = (
            'created',
            'data',
            'id',
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.create_nested_objects(validated_data)
        return instance

    @transaction.atomic
    def create_nested_objects(self, validated_data):
        try:
            company = self.create_company(
                export_status=validated_data['data']['export_status'],
                name=validated_data['data']['company_name'],
                number=validated_data['data']['company_number'],
                date_of_creation=validated_data['data']['date_of_creation'],
                contact_details=validated_data['data']['contact_details'],
            )
            self.create_supplier(
                company=company,
                sso_id=validated_data['data']['sso_id'],
                company_email=validated_data['data']['company_email'],
            )
        except KeyError as error:
            raise serializers.ValidationError(
                'Missing key: "{key}"'.format(key=error)
            )

    def create_company(
        self, name, number, export_status, date_of_creation, contact_details
    ):
        serializer = CompanySerializer(data={
            'name': name,
            'number': number,
            'export_status': export_status,
            'date_of_creation': date_of_creation,
            'contact_details': contact_details,
        })
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def create_supplier(
            self, sso_id, company_email, company):
        serializer = SupplierSerializer(data={
            'sso_id': sso_id,
            'company_email': company_email,
            'company': company.pk,
        })
        serializer.is_valid(raise_exception=True)
        return serializer.save()


class SMSVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
