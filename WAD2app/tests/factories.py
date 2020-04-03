import random
import string

import factory
from factory import fuzzy
from django.test import TestCase

from ..models import *

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

    user = factory.SubFactory(UserFactory)
    breed = factory.Faker('first_name')
    size = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
    age = factory.fuzzy.FuzzyChoice(AGES, getter=lambda c: c[0])
    gender = factory.fuzzy.FuzzyChoice(GENDERS, getter=lambda c: c[0])
    houseTrained = factory.Faker('boolean')
    energyLevel = factory.fuzzy.FuzzyChoice(ENERGY, getter=lambda c: c[0])


class LifeFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserLife

    user = factory.SubFactory(UserFactory)
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

class DogFactory(factory.DjangoModelFactory):
    #missing fields
    class Meta:
        model = models.Dog

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.favourites.add(user)
