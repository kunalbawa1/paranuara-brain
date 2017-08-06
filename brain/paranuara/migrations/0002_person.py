# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import json
from django.utils.dateparse import parse_datetime
from brain.settings import PEOPLE_RESOURCE, VEGETABLES, FRUITS
from paranuara.models import Company
import json

def load_people(apps, schema_editor):
    """ Function to load people data from the resources. """
    Person = apps.get_model("paranuara", "Person")
    try:
        # Read json file
        with open(PEOPLE_RESOURCE) as json_data:
            people = json.load(json_data)
            for person in people:
                # Attempt to convert balance into float
                try:
                    float_balance = float(
                        person['has_died'].replace('$', '').replace(',', ''))
                except:
                    float_balance = 0

                # Attempt to retrieve the company from the db based on the index
                try:
                    company_id = Company.objects.get(index=person['company_id']).id
                except:
                    company_id = None

                # Attempt to convert registered datetime str into datetime
                try:
                    registered_date = parse_datetime(
                        person['registered'].replace(' ', ''))
                except:
                    registered_date = None

                # Attempt to find fav fruits and vegetables
                fruits = []
                vegetables = []
                try:
                    for food in person['favouriteFood']:
                        if food in VEGETABLES:
                            vegetables.append(food)
                        elif food in FRUITS:
                            fruits.append(food)
                except:
                    pass

                p = Person(
                    index=person.get('index'),
                    username=person.get('email'),
                    died=person.get('has_died'),
                    balance=float_balance,
                    picture=person.get('picture'),
                    age=person.get('age'),
                    eye_color=person.get('eyeColor'),
                    name=person.get('name'),
                    gender=person.get('gender'),
                    company_id=company_id,
                    email=person.get('email'),
                    phone=person.get('phone'),
                    address=person.get('address'),
                    description=person.get('about'),
                    registered_date=registered_date,
                    fruits=json.dumps(fruits),
                    vegetables=json.dumps(vegetables)
                )
                p.save()
    except Exception, e:
        print "Error: Failed to load the person data from resources: %s" % e

class Migration(migrations.Migration):

    dependencies = [
        ('paranuara', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('died', models.BooleanField()),
                ('balance', models.FloatField(blank=True)),
                ('picture', models.CharField(max_length=32, blank=True)),
                ('age', models.IntegerField(blank=True)),
                ('eye_color', models.CharField(max_length=16, blank=True)),
                ('name', models.CharField(max_length=64, blank=True)),
                ('gender', models.CharField(max_length=16, blank=True)),
                ('email', models.CharField(max_length=64, blank=True)),
                ('phone', models.CharField(max_length=64, blank=True)),
                ('address', models.CharField(max_length=256, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('registered_date', models.DateTimeField()),
                ('greetings_msg', models.CharField(max_length=128, blank=True)),
                ('tags', models.TextField(default=b'', blank=True)),
                ('fruits', models.TextField(default=b'', blank=True)),
                ('vegetables', models.TextField(default=b'', blank=True)),
                ('company', models.ForeignKey(blank=True, to='paranuara.Company', null=True)),
            ],
        ),

        # Load people from the resources
        migrations.RunPython(load_people),
    ]
