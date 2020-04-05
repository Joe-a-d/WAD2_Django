import random,string,factory
from factory import fuzzy
from WAD2app.choices import *
from WAD2app.models import *


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'username{0}'.format(n))

    password = factory.PostGenerationMethodCall('set_password', factory.Faker('password'))
    email = factory.Faker('email')
    is_staff = factory.Faker('boolean')


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    postcode = factory.Faker('postcode')
    building = factory.Faker('building_number')
    address = factory.Faker('street_name')
    phone = factory.Faker('phone_number')

class PrefFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserPref
        django_get_or_create = ('user',)

    user = factory.SubFactory(ProfileFactory)
    breed = factory.Faker('first_name')
    size = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
    age = factory.fuzzy.FuzzyChoice(AGES, getter=lambda c: c[0])
    gender = factory.fuzzy.FuzzyChoice(GENDERS, getter=lambda c: c[0])
    houseTrained = factory.Faker('boolean')
    energyLevel = factory.fuzzy.FuzzyChoice(ENERGY, getter=lambda c: c[0])


class LifeFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserLife
        django_get_or_create = ('user',)

    user = factory.SubFactory(ProfileFactory)
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
    class Meta:
        model = Dog


    name =  factory.Faker('first_name')
    image = "image.jpg"
    breed = factory.Faker('first_name')
    size = factory.fuzzy.FuzzyChoice(SIZES, getter=lambda c: c[0])
    age = factory.fuzzy.FuzzyChoice(AGES, getter=lambda c: c[0])
    gender = factory.fuzzy.FuzzyChoice(GENDERS, getter=lambda c: c[0])
    houseTrained = factory.Faker('boolean')
    energyLevel = factory.fuzzy.FuzzyChoice(ENERGY, getter=lambda c: c[0])
    isAvailable = factory.Faker('boolean')
    isReserved = factory.Faker('boolean')
    scoresField = factory.RelatedFactory(PrefFactory)
    favourite = factory.RelatedFactory(UserFactory)

class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Application
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    dog = factory.SubFactory(DogFactory)

    created_at = factory.Faker('date_time_this_year', before_now=False)
    updated_at = factory.Faker('date_time_this_year', after_now=True)
    accepted = factory.Faker('boolean')
    approved = factory.Faker('boolean')

class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    application = factory.SubFactory(ApplicationFactory)
    type = factory.fuzzy.FuzzyChoice(TYPES, getter=lambda c: c[0])
    start = factory.Faker('date_time_this_year', )
    end = factory.Faker('date_time_this_year', before_now=False)

    # ignore dynamic save
    title = factory.Faker('first_name')


class ScoresFactory(factory.DjangoModelFactory):
    class Meta:
        model = Scores
        # unique_together=[('user', 'dog')]

    user = factory.SubFactory(PrefFactory)
    dog = factory.SubFactory(DogFactory)
    score = random.randint(0, 5)

class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Messages

    application = factory.SubFactory(ApplicationFactory)
    sender = factory.SubFactory(UserFactory)
    to = factory.SubFactory(UserFactory)
    message = factory.Faker('paragraph')
    created_at = factory.Faker('date_time_this_year', before_now=False)
