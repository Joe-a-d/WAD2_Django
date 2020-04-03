from django import forms
from  .models import *
from django.contrib.auth.models import User


#forms.Form -> forms which do not necessarily interact with DB (email, password)
#forms.ModelForm -> used to directly add or edit a Django model, inherits all from its model

class UserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password',)

class UserProfileForm(forms.Form):

    class Meta:
        model = UserProfile
        exclude = []



class UserLifeForm(forms.ModelForm):

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
