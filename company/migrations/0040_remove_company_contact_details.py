# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-14 17:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0039_company_date_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='contact_details',
        ),
    ]
