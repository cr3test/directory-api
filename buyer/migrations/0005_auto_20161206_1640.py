# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-06 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0004_auto_20161201_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='sector',
            field=models.CharField(choices=[('AEROSPACE', 'Aerospace'), ('AGRICULTURE_HORTICULTURE_AND_FISHERIES', 'Agriculture, horticulture and fisheries'), ('AIRPORTS', 'Airports'), ('AUTOMOTIVE', 'Automotive'), ('BIOTECHNOLOGY_AND_PHARMACEUTICALS', 'Biotechnology and pharmaceuticals'), ('BUSINESS_AND_CONSUMER_SERVICES', 'Business and consumer services'), ('CHEMICALS', 'Chemicals'), ('CLOTHING_FOOTWEAR_AND_FASHION', 'Clothing, footwear and fashion'), ('COMMUNICATIONS', 'Communications'), ('CONSTRUCTION', 'Construction'), ('CREATIVE_AND_MEDIA', 'Creative and media'), ('DEFENCE', 'Defence'), ('EDUCATION_AND_TRAINING', 'Education and training'), ('ELECTRONICS_AND_IT_HARDWARE', 'Electronics and IT hardware'), ('ENVIRONMENT', 'Environment'), ('FINANCIAL_AND_PROFESSIONAL_SERVICES', 'Financial and professional services'), ('FOOD_AND_DRINK', 'Food and drink'), ('GIFTWARE_JEWELLERY_AND_TABLEWARE', 'Giftware, jewellery and tableware'), ('GLOBAL_SPORTS_INFRASTRUCTURE', 'Global sports infrastructure'), ('HEALTHCARE_AND_MEDICAL', 'Healthcare and medical'), ('HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS', 'Household goods, furniture and furnishings'), ('LEISURE_AND_TOURISM', 'Leisure and tourism'), ('MARINE', 'Marine'), ('MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING', 'Mechanical electrical and process engineering'), ('METALLURGICAL_PROCESS_PLANT', 'Metallurgical process plant'), ('METALS_MINERALS_AND_MATERIALS', 'Metals, minerals and materials'), ('MINING', 'Mining'), ('OIL_AND_GAS', 'Oil and gas'), ('PORTS_AND_LOGISTICS', 'Ports and logistics'), ('POWER', 'Power'), ('RAILWAYS', 'Railways'), ('RENEWABLE_ENERGY', 'Renewable energy'), ('RETAIL_AND_LUXURY', 'Retail and luxury'), ('SECURITY', 'Security'), ('SOFTWARE_AND_COMPUTER_SERVICES', 'Software and computer services'), ('TEXTILES_INTERIOR_TEXTILES_AND_CARPETS', 'Textiles, interior textiles and carpets'), ('WATER', 'Water')], max_length=255),
        ),
    ]
