from rest_framework import serializers

from company import models, validators


class CompanyCaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyCaseStudy
        fields = (
            'pk',
            'company',
            'description',
            'image_one',
            'image_three',
            'image_two',
            'keywords',
            'sector',
            'testimonial',
            'title',
            'video_one',
            'website',
            'year',
        )

    def validate_website(self, value):
        return value or ''

    def validate_testimonial(self, value):
        return value or ''


class CompanyCaseStudyWithCompanySerializer(CompanyCaseStudySerializer):
    class Meta(CompanyCaseStudySerializer.Meta):
        depth = 2


class CompanySerializer(serializers.ModelSerializer):

    id = serializers.CharField(read_only=True)
    date_of_creation = serializers.DateField()
    sectors = serializers.JSONField(required=False)
    logo = serializers.ImageField(
        max_length=None, allow_empty_file=False, use_url=True, required=False
    )
    supplier_case_studies = CompanyCaseStudySerializer(
        many=True, required=False, read_only=True
    )

    class Meta(object):
        model = models.Company
        fields = (
            'date_of_creation',
            'description',
            'employees',
            'export_status',
            'id',
            'keywords',
            'logo',
            'name',
            'number',
            'revenue',
            'sectors',
            'supplier_case_studies',
            'website',
        )

    def validate_website(self, value):
        return value or ''

    def validate_description(self, value):
        return value or ''


class CompanyNumberValidatorSerializer(serializers.Serializer):
    number = serializers.CharField(validators=[
        validators.company_unique,
    ])


class VerifyCompanyWithCodeSerializer(serializers.Serializer):

    sso_user_id = serializers.CharField()
    code = serializers.CharField()
