import random
import string

import factory
from django.test import TestCase

from .models import *

class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker('username')
    password = factory.Faker('password')
    email = factory.Faker('email')


class ProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    postcode = factory.Faker('postcode')
    building = factory.Faker('building_number')
    address = factor.Faker('street_name')
    phone = factory.Faker('phone_number')

class PrefFactory(factory.Factory):
    class Meta:
        model = UserPref

        user = factory.SubFactory(UserFactory)
        breed = factory.Faker('first_name')
        size = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
        age = factory.fuzzy.FuzzyChoice(AGES, getter=lambda c: c[0])
        gender = factory.fuzzy.FuzzyChoice(GENDERS, getter=lambda c: c[0])
        houseTrained = factory.Faker('boolean')
        energyLevel = factory.fuzzy.FuzzyChoice(ENERGY, getter=lambda c: c[0])


class LifeFactory(factory.Factory):
    class Meta:
        model = UserLife

        user = factory.SubFactory(UserFactory)
        lifestyle = factory.fuzzy.FuzzyChoice(UserLife.pENERGY, getter=lambda c: c[0])
        timeAway =
        house = factory.fuzzy.FuzzyChoice(UserLife.HOUSES, getter=lambda c: c[0])
        garden = factory.Faker('boolean')
        hasCat = factory.Faker('boolean')
        hasDog = factory.Faker('boolean')
        cohab = random.randint(0, 20)
        hasChildren = factory.Faker('boolean')
        trainer = factory.Faker('boolean')
        dogOwner = factory.Faker('boolean')
