# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import json
from brain.settings import COMPANY_RESOURCE

def load_companies(apps, schema_editor):
    """ Function to load the default company data from the resources. """
    Company = apps.get_model("paranuara", "Company")
    try:
        # Read json file
        with open(COMPANY_RESOURCE) as json_data:
            companies = json.load(json_data)
            for company in companies:
                c = Company(index=company['index'], name=company['company'])
                c.save()
    except Exception, e:
        print "Error: Failed to load the company data from resources: %s" % e

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('index', models.IntegerField(unique=True)),
            ],
        ),

        # Load the companies from the resources
        migrations.RunPython(load_companies),
    ]
