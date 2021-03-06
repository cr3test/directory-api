# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-03 16:01
from __future__ import unicode_literals

from django.db import migrations
from django.core import management

from elasticsearch_dsl import Index, analyzer

from company.search import CompanyDocType


def add_company_search_index_and_populate(apps, schema_editor):
    companies = Index('companies')
    if not companies.exists():
        companies.doc_type(CompanyDocType)
        companies.analyzer(analyzer('english'))
        companies.create()
    management.call_command('populate_elasticsearch')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0043_auto_20170505_1148'),
    ]

    operations = [
        migrations.RunPython(
            add_company_search_index_and_populate,
            noop
        )
    ]
