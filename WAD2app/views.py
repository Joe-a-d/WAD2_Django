from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from WAD2app.forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm



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

def calcScore():
    # iterate through userPreferences & dogTraits
    # counter++ if in uP & dog
    # save as dog attribute score : {userId : (score1, score2), ...}
    # retrieve on render with dog.score[userId][score1]/[score2]
    # use score1 to display on dog profiles and score2 for staff/applications
