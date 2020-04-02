from django import forms
from  .models import *
from django.contrib.auth.models import User


#forms.Form -> forms which do not necessarily interact with DB (email, password)
#forms.ModelForm -> used to directly add or edit a Django model, inherits all from its model

class UserProfileForm(forms.Form):
    #PLACEHOLDER
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserLifeForm(forms.ModelForm):
    #PLACEHOLDER
    class Meta:
        model = UserLife
        exclude = []

class UserPrefForm(forms.ModelForm):
    try:
        inSHELTER = [(i,x.breed) for i,x in enumerate(Dog.objects.exclude(isAvailable=False).distinct())]
    except:
        inSHELTER = []

    breed = forms.MultipleChoiceField(choices=inSHELTER, widget=forms.CheckboxSelectMultiple, help_text="You'll only be able to select breeds of dogs currently in the shelter, but you can check back later and edit your preferences on your profile page")
    age = forms.MultipleChoiceField()
    gender = forms.MultipleChoiceField()
    energyLevel = forms.MultipleChoiceField()
    size = forms.MultipleChoiceField()
    houseTrained = forms.BooleanField()


    class Meta:
        model = UserProfile
        exclude = []

class DogForm(forms.ModelForm):
    #PLACEHOLDER
    class Meta:
        model = Dog
        exclude = []


class dateForm(forms.Form):
    start = models.DateTimeField()
    # needs validation, popup FullCallendar prob better option

class EventForm(forms.ModelForm):
    #PLACEHOLDER
    class Meta:
        model = Event
        exclude = []

class ContactForm(forms.Form):
    #PLACEHOLDER
    pass
