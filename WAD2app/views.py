from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import make_password
from django.conf import settings
from WAD2.settings import EMAIL_HOST_USER
from .forms import *
from .filters import *
from .models import *
from datetime import datetime, timedelta


def home(request):
    return render(request, 'wad2App/home.html')

def about(request):
    return render(request, "wad2App/about.html")

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, [EMAIL_HOST_USER])
                messages.success(request, 'Thanks for getting in touch!')
                return redirect('WAD2app:contact')
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return render(request, 'contact.html', {'form': form})
    return render(request, "wad2App/contact.html", {'form': form})

##################### USER ####################
# signup
def register(request):
    #for debugging
    registered = False
    noProfile = request.user.is_superuser

    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('WAD2app:profile')


    if request.method == 'POST' :
        user_form = UserForm(request.POST)


        if user_form.is_valid():

            formUser = user_form.save()
            formUser.password = make_password(user_form.cleaned_data['password'])

            if noProfile:
                formUser.is_staff = True
                formUser.save()
                return redirect('WAD2app:dashboard')
            if profile_form.is_valid():
                profile = profile_form.save(commit = False)
                profile.user = formUser
                profile.save()
                messages.success(request, 'Your account has been successfully created!. Now please create your profile, so that we are able to match you with your 4-legged buddy!')
                return redirect('WAD2app:registerProfile', id=user.id)

            registered = True

            messages.success(request, 'Staff account has been successfully created!.')


        else:
            messages.error(request, 'Something went wrong while trying to register your account. Please try again.')
    else:
        user_form = UserForm()
        if noProfile:
            return render(request, 'wad2App/users/register.html', context = {'user_form': user_form,})
        profile_form = UserProfileForm()

    return render(request, 'wad2App/users/register.html', context = {'user_form': user_form, 'profile_form': profile_form})


def registerProfile(request, id):
    if request.user.is_authenticated:
        return redirect('WAD2app:profile')

    if request.method == 'POST':
        user = User.objects.get(id=id)
        profile = UserProfile.objects.get(user=user)
        pref_form = UserPrefForm(request.POST)
        life_form = UserLifeForm(request.POST)


        if  pref_form.is_valid() and life_form.is_valid():
            pref = pref_form.save(commit = False)
            life = life_form.save(commit = False)

            pref.user = profile
            life.user = profile

            pref.save()
            life.save()

            messages.success(request, "You're all set! Login to enjoy all our webpage has to offer")

            return redirect('WAD2app:login')
        else:
            messages.error(request, 'Something went wrong while trying to save your profile. Please try again.')
    else:

        pref_form = UserPrefForm()
        life_form = UserLifeForm()

    return render(request, 'wad2App/users/registerProfile.html',context = { "pref_form": pref_form , "life_form":life_form , "id":id})

def editProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            dogs = Dog.objects.all()
            calcNewUser(user, dogs, False)
            registered = True
            messages.success(request, 'Your profile has been updated!')
            return redirect('wad2App/users/profile')

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

def user_login(request):
    if request.user.is_authenticated :
        if request.user.is_staff:
            messages.error(request, "You are already logged in")
            return redirect(reverse('WAD2app:dashboard'))
        messages.error(request, "You are already logged in")
        return redirect(reverse('WAD2app:profile'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return redirect('WAD2app:dashboard')
                return redirect('WAD2app:profile')
            else:
                messages.error(request, "We couldn't log you in. Please contact us directly")
                return redirect('wad2App/about.html')
        else:
            print(f'Invalid login details: {username}, {password}')
            return render(request, 'wad2App/users/login.html',)
    else:
        return render(request, 'wad2App/users/login.html',)

@login_required
def user_logout(request):
    logout(request)
    return redirect('WAD2app:home')


@login_required
def profile(request):
    context_dict = {}
    profile = UserProfile.objects.get(user = request.user)
    favourites = Dog.objects.filter(favourites = request.user)
    application = Application.objects.filter(user = request.user)
    context_dict['profile'] = profile
    context_dict['favourites'] = favourites
    context_dict['application'] = application
    print(context_dict)
    return render(request, 'wad2App/users/profile.html', context_dict)

@staff_member_required
def dashboard(request):
    context_dict = {}

    context_dict['applications'] = Application.objects.all()

    return render(request, 'wad2App/staff/dashboard.html', context_dict)

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
                dog.scoresField.add(person, through_defaults={'score':score})
            messages.success(request, f'{name} has been added to the list of available dogs!')
            return redirect('WAD2app:dogs')

    else:
        dog_form = DogForm()

    return render(request, 'wad2App/dogs/addDog.html', context = {'dog_form': dog_form})


def dog(request, pk):
    dog = Dog.objects.get(pk=pk)
    user_filter = ['id','image','isAvailable', 'isReserved']
    #dateForm = dateForm()
    if 'delete' in request.POST:
        dog.delete()
    return render(request, 'wad2App/dogs/dog.html', context={'dog': dog, 'dateForm': dateForm, 'user_filter': user_filter})

def dogs(request):
    #f = DogFilter(request.GET, queryset=Dog.objects.all())
    dogs = Dog.objects.all()
    return render(request, 'wad2App/dogs/dogs.html', {'dogs':dogs})#, {'filter': f})

@login_required
def showApplication(request, id):
    user = request.user
    try:
        app_user = User.objects.get(id=id)
        app = Application.objects.filter(user=app_user)
    except:
        messages.error(request, 'We could not find that application!')
        return redirect(reverse('WAD2app:home'))
    try:
        user_messages = getMessages(request, app_user)
    except:
        messages.error(request, "Oops, it seems like we can't show you your messages at the moment")

    context = {}
    context['fullData'] = user_messages
    context['msgs'] = user_messages['thread']
    context['app'] = app
    print(context)
    return render(request, 'wad2App/application.html', context)

######################## AJAX ########################

@login_required
def favourite(request):
    dog_id = request.get("dog_id")
    fav = request.get("fav")
    user = request.user


    try:
        Dog.objects.get(id=dog_id)
        if fav:
            dog.favourites.add(user)
            added = user in dog.favourites.all()
        else:
            dog.favourites.delete(user)
            removed = user not in dog.favourites.all()
    except:
        added = False

        data = {
        'added': added,
        'removed': removed
    }
    return JsonResponse(data)


@login_required
def adopt(request):
    user = request.user
    dog = Dogs.object.get(id=request.get("dog_id"))
    start = request.get("start")
    #parse dates into ISO_8601 strings
    start = datetime.strptime(start, '%d,%m,%y,%H,%M')
    end = start + datetime.timedelta(minutes=30)

    app,created = Application.objects.get_or_create(user=user, dog=dog)
    event  = Event.objects.get_or_create(application = app, type="FIRST",start=start, end=end)

    if created:
         data = {
        'created': created
        }
    return JsonResponse(data)


@login_required
def updateApplication(request, id):
    user = User.objects.get(id=id)
    app = Application.objects.get(user=user)

    if request.get('accept'):
        application.accepted = True
        application.save()
    if request.get('approved'):
        application.approved = True
        application.delete()
    if request.get('reschedule'):
        pass


    return render(request, 'rango/application.html', {'application' : application},)


######################## HELPERS ########################

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

    return (score/len(fields))*100

def calcNewUser(user, dogs, new):
    for dog in dogs:
        score = calc(user, dog)
        if not new:
            dog.scoresField.remove(user)
        dog.scoresField.add(user, through_defaults={'score':score})

######################## MESSAGES ########################
@login_required
def sendMessage(request, app_user):
    user = request.user
    staff = [user for user in User.objects.all() if user.is_staff]
    if request.method == 'POST':
        if user == app_user:
            to = staff
        else:
            #avoids having to check length before iteration
            to = [user]
        sender = user
        message = MessageForm(request.POST)
        if message.is_valid():
            content = message.cleaned_data['message']
            for user in to:
                Messages.objects.create(sender=sender, to=user, message=content)
        else:
            messages.error(f"We could not send your message. Try again or email us directly on {settings.EMAIL_HOST_USER}")
    else:
        message = MessageForm()
    return render(request, 'rango/index.html', {'message': message})

@login_required
def getMessages(request, app_user):
    context_dict = {}
    inbox = Messages.objects.filter(to = app_user)
    sent = Messages.objects.filter(sender = app_user)
    thread = inbox.union(sent).order_by('created_at')

    context_dict["inbox"] = inbox
    context_dict["sent"] = sent
    context_dict["thread"] = thread
    print(context_dict)
    return context_dict

######################## FullCallendar ########################
def getEvents(request):
    events = Events.objects.all()
    return render(request,'calendar.html',{"events": events})

def updateEvent(request):
    id = request.GET.get("id", None)
    start = request.GET.get("start", None)

    try:
        event = Events.objects.get(id=id)
        event.save()
        messages.success(request, 'Event updated!')
    except:
        messages.error(request, 'Failure to update the event!')

    return redirect(reverse("WAD2app:calendar"))

def delEvent(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()

    subject = "Appointment Cancelation"
    email = event.application.user.profile.email
    message = "Unfortunately we had to cancel your appointment. Please get in touch with us if you want to reschedule it"
    send_mail(subject, message, email)
    return redirect(reverse("WAD2app:calendar"))
