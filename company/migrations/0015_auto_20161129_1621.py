# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-29 16:21
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_company_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AlterModelOptions(
            name='companycasestudy',
            options={'get_latest_by': 'modified', 'ordering': ('-modified', '-created')},
        ),
        migrations.AddField(
            model_name='company',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='company',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='companycasestudy',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='companycasestudy',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='modified'),
        ),
    ]
