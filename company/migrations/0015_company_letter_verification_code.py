# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-29 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_company_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='letter_verification_code',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='letter verification code'),
        ),
    ]
