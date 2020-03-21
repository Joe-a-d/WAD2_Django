from django import forms
from  .models import *
from django.contrib.auth.models import User


#forms.Form -> forms which do not necessarily interact with DB (email, password)
#forms.ModelForm -> used to directly add or edit a Django model, inherits all from its model

class UserProfileForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserPrefForm(forms.ModelForm):
    try:
        inSHELTER = [(i,x.breed) for i,x in enumerate(Dog.objects.exclude(isAvailable=False).distinct())]
    except:
        inSHELTER = []

    breed = forms.MultipleChoiceField(choices=inSHELTER, widget=forms.CheckboxSelectMultiple, help_text="You'll only be able to select breeds of dogs currently in the shelter, but you can check back later and edit your preferences on your profile page")
    age = forms.MultipleChoiceField()
    gender = forms.MultipleChoiceField()
    energyLevel = forms.MultipleChoiceField()

    class Meta:
        model = UserProfile
        exclude = []
