from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import *
from .filters import *

def home(request):
    return render(request, 'WAD2app/home.html')

def about(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail(subject, message, email)
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return render(request, 'about.html', {'form': form})
            messages.success(request, 'Thanks for getting in touch!')
            return redirect('wad2App/about.html')
    return render(request, "wad2App/about.html", {'form': form})

##################### USER ####################
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

    return render(request, 'wad2App/users/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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

    return render(request, 'wad2App/users/profile.html', context)


def donate(request):
    return render(request, "wad2App/donate.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('wad2App:profile'))
            else:
                messages.error(request, "We couldn't log you in. Please contact us directly")
                return redirect('wad2App/about.html')
        else:
            print(f'Invalid login details: {username}, {password}')
            return render(request, 'wad2App/login.html')
    else:
        return render(request, 'wad2App/login.html')

@login_required
def profile(request):
    return render(request, 'WAD2app/profile.html')

@staff_member_required
def dashboard(request):
    return render(request, 'WAD2app/dashboard.html')

############ DOGS ##########
@staff_member_required
def addDog(request):
    people = UserPref.objects.all()
    if request.method == 'POST':
        dog_form = DogForm(request.POST,request.FILES,)
        if dog_form.is_valid():
            name = request.POST.get('name')
            dog = dog_form.save().pk
            for person in people:
                score = calc(person, dog)
                dog.score.add(person, through_defaults={'score':score})
            messages.success(request, f'{name} has been added to the list of available dogs!')
            return redirect('wad2App:dogs')

    else:
        dog_form = DogForm()

    return render(request, 'wad2App/addDog.html', context = {'dog_form': dog_form})


def dog(request, pk):
    dog = Dogs.objects.get(pk=pk)
    return render(request, 'WAD2app/dog.html', {'dog': dog})

def dogs(request):
    f = DogFilter(request.GET, queryset=Dogs.objects.all())
    return render(request, 'wad2App/dogs.html', {'filter': f})

#############################

@login_required
def favourite(request, pk):
    if request.method == 'POST':
        UserPref.favourites.add(pk)
        messages.success("Added to favourites!")
        return redirect('wad2App:dogs')
    else:
        messages.error("We couldn't add it to your favourites. Please, try again")
    return render(request,)

@login_required
def adopt(request):
    return HttpResponse('<h1>TEST</h1>')

######################### HELPERS ##################

def calc(user, dog):
    fields = ["breed", "size", "age", "gender", "houseTrained", "energyLevel"]
    score = 0

    for field in fields:
        try:
            value = getattr(user,field)
            if value == "Any":
                score += 1
                continue
            elif value == getattr(dog,field):
                score += 1
# check only not null preferences , prevents skewed averages
        except:
            score += 1
            continue

    return score
# 
# def calcNewUser(user, dogs):
#     for dog in dogs:
#         score = calc(user, dog)
#         dog.
