# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-10 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0007_auto_20170112_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierEmailNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('no_case_studies', 'Case studies not created'), ('hasnt_logged_in', 'Not logged in after first 30 days'), ('verification_code_not_given', 'Verification code not supplied')], max_length=255)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
