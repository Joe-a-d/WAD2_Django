from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .choices import *
from django.core.validators import MaxValueValidator, MaxLengthValidator, MinValueValidator
import datetime




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField (upload_to='profileImages' , blank=True, default=settings.STATIC_URL+'profileImg')
    postcode = models.CharField( max_length=10)
    building = models.IntegerField( validators=[MaxValueValidator(1000)])
    address = models.CharField( max_length=300)
    phone = models.IntegerField()



##################### USER #####################
class UserPref(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    breed = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField( max_length=10,choices=SIZES, default="ANY", blank=True, null=True)
    age = models.CharField(max_length=10,choices=AGES, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True, null=True)
    houseTrained = models.NullBooleanField( blank=True, null=True)
    energyLevel = models.CharField(max_length=20,choices=ENERGY, blank=True, null=True)


class UserLife(models.Model):
    pENERGY = [("H", "Active"), ("M", "Average"), ("L", "Sedentary")]
    HOUSES = [("APT", "Apartment"), ("HO", "House")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="life")
    lifestyle = models.CharField(max_length=10,choices=pENERGY)
    timeAway = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)], )
    house = models.CharField(max_length=10,choices=HOUSES)
    garden = models.BooleanField()
    hasCat = models.BooleanField()
    hasDog = models.BooleanField()
    cohab = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(10)])
    hasChildren = models.BooleanField( )
    trainer = models.BooleanField()
    dogOwner = models.BooleanField()


##################### DOG #####################

class Dog(models.Model):

    name = models.CharField(max_length=20)
    image = models.ImageField (upload_to='dogImages' , default=settings.STATIC_URL+'dogImg')
    size = models.CharField( max_length=10,choices=SIZES, default="ANY",)
    breed = models.CharField(max_length=20)
    age = models.CharField(max_length=10,choices=AGES,)
    gender = models.CharField(max_length=10, choices=GENDERS,)
    houseTrained = models.NullBooleanField(default=True,)
    energyLevel = models.CharField(max_length=20,choices=ENERGY,)

    isAvailable = models.BooleanField(default=True)
    isReserved = models.BooleanField(default=False)
    scoresField = models.ManyToManyField(UserPref, through='Scores',through_fields=('dog', 'user'),)
    favourites = models.ManyToManyField(User, related_name="favourites",)

##################### OTHERS #####################

class Application(models.Model):

     user = models.OneToOneField(User, on_delete=models.CASCADE)
     dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     accepted = models.BooleanField(default=False)
     approved = models.BooleanField(default=False)

class Event(models.Model):
    TYPES = [("FIRST", "First Visit"), ("COURSE", "Course"), ("GEN", "General Visit"), ("ADOPT", "Pickup Pet")]

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=TYPES)
    title = models.CharField(max_length=20,)
    start = models.DateTimeField()
    end = models.DateTimeField() #fix end, 30min gap, start returns datetime.datetime

    def save(self, *args, **kwargs):
        subject = "Your scheduled visit to RightPet"
        message = f"Your visit was scheduled for {self.start} ."
        mail = self.application.user.email
        send_mail(subject, message, email)
        super().save(*args, **kwargs)

class Scores(models.Model):
    user = models.ForeignKey(UserPref, on_delete=models.CASCADE, related_name="hasScores")
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together=[('user', 'dog')]

class Messages(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
