import os, django,random,string,factory
from factory import fuzzy
from wad2App.models import *
from WAD2app.choices.py import *


import django
import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2.settings')
django.setup()



class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('first_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    postcode = factory.Faker('postcode')
    building = factory.Faker('building_number')
    address = factory.Faker('street_name')
    phone = factory.Faker('phone_number')

class PrefFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserPref

    user = factory.SubFactory(UserProfileFactory)
    breed = factory.Faker('first_name')
    size = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
    age = factory.fuzzy.FuzzyChoice(AGES, getter=lambda c: c[0])
    gender = factory.fuzzy.FuzzyChoice(GENDERS, getter=lambda c: c[0])
    houseTrained = factory.Faker('boolean')
    energyLevel = factory.fuzzy.FuzzyChoice(ENERGY, getter=lambda c: c[0])


class LifeFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserLife

    user = factory.SubFactory(UserProfileFactory)
    lifestyle = factory.fuzzy.FuzzyChoice(UserLife.pENERGY, getter=lambda c: c[0])
    timeAway = random.randint(0, 30)
    house = factory.fuzzy.FuzzyChoice(UserLife.HOUSES, getter=lambda c: c[0])
    garden = factory.Faker('boolean')
    hasCat = factory.Faker('boolean')
    hasDog = factory.Faker('boolean')
    cohab = random.randint(0, 20)
    hasChildren = factory.Faker('boolean')
    trainer = factory.Faker('boolean')
    dogOwner = factory.Faker('boolean')

class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Appplication

     user = factory.SubFactory(UserProfileFactory)
     dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

     created_at = factory.Faker('date_time_this_year', before_now=False)
     updated_at = factory.Faker('date_time_this_year', after_now=True)
     accepted = factory.Faker('boolean')
     approved = factory.Faker('boolean')

class Event(factory.DjangoModelFactory):
    class Meta:
        model = Event

    TYPES = [("FIRST", "First Visit"), ("COURSE", "Course"), ("GEN", "General Visit"), ("ADOPT", "Pickup Pet")]

    application = factory.SubFactory(ApplicationFactory)
    type = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
    start = factory.Faker('date_time_this_year', )
    end = factory.Faker('date_time_this_year', before_now=False)


class Scores(factory.DjangoModelFactory):
    class Meta:
        model = Scores
        unique_together=[('user', 'dog')]

    user = factory.SubFactory(UserFactory)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    score = random.randint(0, 5)




class Messages(factory.DjangoModelFactory):
    class Meta:
        model = Messages

    application = factory.SubFactory(ApplicationFactory)
    sender = factory.SubFactory(UserFactory)
    to = factory.SubFactory(UserFactory)
    message = factory.Faker('paragraph')
    created_at = factory.Faker('date_time_this_year', before_now=False)
