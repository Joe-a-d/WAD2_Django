from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MaxLengthValidator, MinValueValidator



# SHARED CONSTANTS

SIZES = [("ANY", "Any"),("S","Small"),("M","Medium"),("L","Large")]
AGES = [("PUP", "Puppy"), (2, "1-2"), (3, "2-5"), (4, "5+")]
GENDERS = [("F", "Female"), ("M", "Male")]
ENERGY = [("H", "Live Wire"), ("M", "Average"), ("L", "Couch Potato")]

class Dog(models.Model):

    name = models.CharField(max_length=20)
    image = models.ImageField (upload_to='dogImages' , default=settings.STATIC_URL+'dogImg')
    size = models.CharField( max_length=10,choices=SIZES, default="ANY",)
    breed = models.CharField(max_length=20)
    age = models.CharField(max_length=10,choices=AGES,)
    gender = models.CharField(max_length=10, choices=GENDERS,)
    houseTrained = models.NullBooleanField()
    energyLevel = models.CharField(max_length=20,choices=ENERGY,)

    isAvailable = models.BooleanField(default=True)
    isReserved = models.BooleanField(default=False)
    score = models.ManyToManyField(UserPref, through='Scores',through_fields=('dog', 'user'), blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField (upload_to='profileImages' , blank=True, default=settings.STATIC_URL+'profileImg')
    postcode = models.CharField( max_length=10)
    building = models.IntegerField( validators=[MaxValueValidator(1000)])
    address = models.CharField( max_length=300)
    phone = models.IntegerField( validators=[MaxLengthValidator(11)])




class UserPref(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length=20,)
    size = models.CharField( max_length=10,choices=SIZES, default="ANY", blank=True, null=True)
    age = models.CharField(max_length=10,choices=AGES, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True)
    houseTrained = models.NullBooleanField( blank=True, null=True)
    energyLevel = models.CharField(max_length=20,choices=ENERGY, blank=True, null=True)

    #RELATIONS
    favourites = models.ManyToManyField(Dog, related_name='favouritedBy', blank=True, null=True)


class UserLife(models.Model):
    pENERGY = [("H", "Active"), ("M", "Average"), ("L", "Sedentary")]
    HOUSES = [("APT", "Apartment"), ("HO", "House")]

    lifestyle = models.CharField(max_length=10,choices=pENERGY)
    timeAway = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)], )
    house = models.CharField(max_length=10,choices=HOUSES)
    garden = models.NullBooleanField()
    hasCat = models.NullBooleanField()
    hasDog = models.NullBooleanField()
    cohab = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(10)])
    hasChildren = models.NullBooleanField( )
    trainer = models.NullBooleanField()
    dogOwner = models.NullBooleanField()




class Application(models.Model):

     user = models.OneToOneField(User, on_delete=models.CASCADE)
     dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     accepted = models.BooleanField(default=False)
     approved = models.BooleanField(default=False)

class Event(models.Model):

    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    title = models.CharField(max_length=20,)
    start = models.DateTimeField()
    end = models.DateTimeField()

class Scores(models.Model):
    user = models.ForeignKey(UserPref, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together=[('user', 'dog')]
