from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserPrefForm
from .filters import *

def dogs(request):
    f = ProductFilter(request.GET, queryset=Dogs.objects.all())
    return render(request, 'wad2App/dogs.html', {'filter': f})


# signup
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #prevents DB integrity errors
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
            messages.success(request, 'Your account has been successfully created! ')
            return redirect('login')
        else:
            print(user_form.errors, profile_form.errors)
            messages.error(request, 'Something went wrong while trying to register your account. Please try again.')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'wad2App/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

# edit profile

def editProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)

def about(request):
    return HttpResponse('<h1>TEST</h1>')

def contact(request):
    return HttpResponse('<h1>TEST</h1>')

def donate(request):
    return HttpResponse('<h1>TEST</h1>')

def login(request):
    return HttpResponse('<h1>TEST</h1>')

def profile(request):
    return HttpResponse('<h1>TEST</h1>')

def dashboard(request):
    return HttpResponse('<h1>TEST</h1>')

def addDog(request):
    return HttpResponse('<h1>TEST</h1>')

def dog(request):
    return HttpResponse('<h1>TEST</h1>')

def favourite(request):
    return HttpResponse('<h1>TEST</h1>')

def adopt(request):
    return HttpResponse('<h1>TEST</h1>')

def home(request):
    return HttpResponse('<h1>TEST</h1>')
