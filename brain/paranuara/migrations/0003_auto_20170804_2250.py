# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import json
from brain.settings import PEOPLE_RESOURCE

def load_friends(apps, schema_editor):
    """ Function to load people's friends data from the resources. """
    Person = apps.get_model("paranuara", "Person")
    PersonFriend = apps.get_model("paranuara", "PersonFriend")
    try:
        # Read json file
        with open(PEOPLE_RESOURCE) as json_data:
            people = json.load(json_data)
            for person in people:
                from_person = Person.objects.get(index=person['index'])
                for friend in person['friends']:
                    to_person = Person.objects.get(index=friend['index'])
                    relationship = PersonFriend(from_person=from_person,
                                                to_person=to_person)
                    relationship.save()
    except Exception, e:
        print "Error: Failed to save the relationships from resources: %s" % e


class Migration(migrations.Migration):

    dependencies = [
        ('paranuara', '0002_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonFriend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_person', models.ForeignKey(related_name='from_people', to='paranuara.Person')),
                ('to_person', models.ForeignKey(related_name='to_people', to='paranuara.Person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='friends',
            field=models.ManyToManyField(to='paranuara.Person', through='paranuara.PersonFriend'),
        ),

        # Load person friends from the resources
        migrations.RunPython(load_friends),
    ]
