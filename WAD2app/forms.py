from django import forms
from  .models import *
from django.contrib.auth.models import User


#forms.Form -> forms which do not necessarily interact with DB (email, password)
#forms.ModelForm -> used to directly add or edit a Django model, inherits all from its model

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class UserProfileForm(forms.Form):

    class Meta:
        model = UserProfile
        exclude = ['user',]



class UserLifeForm(forms.ModelForm):

    class Meta:
        model = UserLife
        exclude = ['user',]

class UserPrefForm(forms.ModelForm):
    try:
        inSHELTER = [(i,x.breed) for i,x in enumerate(Dog.objects.exclude(isAvailable=False).distinct())]
    except:
        inSHELTER = []

    breed = forms.MultipleChoiceField(choices=inSHELTER,help_text="You'll only be able to select breeds of dogs currently in the shelter, but you can check back later and edit your preferences on your profile page", required=False,)
    age = forms.MultipleChoiceField(required=False,)
    gender = forms.MultipleChoiceField(required=False,)
    energyLevel = forms.MultipleChoiceField(required=False,)
    size = forms.MultipleChoiceField(required=False,)
    houseTrained = forms.BooleanField(required=False,)


    class Meta:
        model = UserProfile
        exclude = ['user',]
        widgets = {forms.CheckboxSelectMultiple,}

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = []

class ProfileUpdateForm(forms.Form):

    class Meta:
        model = User
        exclude = []

class DogForm(forms.ModelForm):

    class Meta:
        model = Dog
        exclude = []


class dateForm(forms.Form):
    start = models.DateTimeField()
    # needs validation, popup FullCallendar prob better option

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = []

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100,)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
