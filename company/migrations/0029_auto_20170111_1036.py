# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-11 10:36
from __future__ import unicode_literals

from django.db import migrations


def set_contact_detials_fields(apps, schema_editor):
    Company = apps.get_model('company', 'Company')
    for company in Company.objects.all():
        details = company.contact_details
        if details:
            company.postal_full_name = details.get('postal_full_name') or ''
            company.address_line_1 = details.get('address_line_1') or ''
            company.address_line_2 = details.get('address_line_2') or ''
            company.address_line_2 = details.get('address_line_2') or ''
            company.locality = details.get('locality') or ''
            company.country = details.get('country') or ''
            company.postal_code = details.get('postal_code') or ''
            company.po_box = details.get('po_box') or ''
            company.mobile_number = details.get('mobile_number') or ''
            company.email_address = details.get('email_address') or ''
            company.email_full_name = details.get('email_full_name') or ''
            company.save()


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0028_auto_20170111_1034'),
    ]

    operations = [
        migrations.RunPython(set_contact_detials_fields)
    ]
