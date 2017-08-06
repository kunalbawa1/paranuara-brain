from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=32)
    index = models.IntegerField(unique=True)

class Person(models.Model):
    index = models.IntegerField(unique=True)
    username = models.CharField(max_length=64, unique=True)
    died = models.BooleanField()
    balance = models.FloatField(blank=True)
    picture = models.CharField(max_length=32, blank=True)
    age = models.IntegerField(blank=True)
    eye_color = models.CharField(max_length=16, blank=True)
    name = models.CharField(max_length=64, blank=True)
    gender = models.CharField(max_length=16, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True, default='')
    registered_date = models.DateTimeField()
    greetings_msg = models.CharField(max_length=128, blank=True)
    tags = models.TextField(blank=True, default='')
    fruits = models.TextField(blank=True, default='')
    vegetables = models.TextField(blank=True, default='')
    friends = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='PersonFriend',

        # this argument is required to define a custom
        # through model for many to many relationship to self
        # position matters: 1 - source (from), 2 - target (to)
        through_fields=('from_person', 'to_person'),
    )

class PersonFriend(models.Model):
    from_person = models.ForeignKey(Person, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(Person, related_name='to_people', on_delete=models.CASCADE)