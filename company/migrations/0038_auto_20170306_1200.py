# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-06 12:00
from __future__ import unicode_literals

from datetime import datetime

from django.db import migrations


def populate_verification_date(apps, schema_editor):
    Company = apps.get_model("company", "Company")
    queryset = Company.objects.filter(
        verified_with_code=True,
        date_verification_letter_sent__isnull=True,
    )
    queryset.update(date_verification_letter_sent=datetime.utcnow())


def noop(*args, **kwargs):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0037_auto_20170306_1154'),
    ]

    operations = [
        migrations.RunPython(populate_verification_date, noop)
    ]
