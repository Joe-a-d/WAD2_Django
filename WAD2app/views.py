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
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            form.save()
            try:
                send_mail(subject, message, email)
            except BadHeaderError:
                messages.error(request, 'Bad header')
                return render(request, 'about.html', {'form': form})
            messages.success(request, 'Thanks for getting in touch!')
            return redirect('wad2App:contact')
    return render(request, "wad2App/contact.html", {'form': form})

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
            dogs = Dog.objects.all()
            calcNewUser(user, dogs, True)
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

def login(request):
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(username=username, password=password)
    #
    #     if user:
    #         if user.is_active:
    #             login(request, user)
    #             return redirect(reverse('wad2App:profile'))
    #         else:
    #             messages.error(request, "We couldn't log you in. Please contact us directly")
    #             return redirect('wad2App/about.html')
    #     else:
    #         print(f'Invalid login details: {username}, {password}')
    #         return render(request, 'wad2App/users/login.html')
    # else:
    #     return render(request, 'wad2App/users/profile.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('wad2App:home'))
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'wad2App/users/login.html')

@login_required
def profile(request):
    return render(request, 'wad2App/users/profile.html')

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
            return redirect('wad2App/dogs/dogs.html')

    else:
        dog_form = DogForm()

    return render(request, 'wad2App/dogs/addDog.html', context = {'dog_form': dog_form})


def dog(request, pk):
    dog = Dogs.objects.get(pk=pk)
    dateForm = dateForm()
    if 'delete' in request.POST:
        dog.delete()
    return render(request, 'wad2App/dogs/dogs.html', {'dog': dog, 'dateForm': dateForm})

def dogs(request):
    f = DogFilter(request.GET, queryset=Dog.objects.all())
    return render(request, 'wad2App/dogs/dogs.html', {'filter': f})

#############################

@login_required
def favourite(request, pk):
    if request.method == 'POST':
        Dog.favourites.add(pk)
        messages.success("Added to favourites!")
        return redirect('wad2App:dogs')
    else:
        messages.error("We couldn't add it to your favourites. Please, try again")
    return render(request,)

@login_required
def adopt(request,pk):
    user = request.user
    dog = Dogs.objects.get(pk=pk)
    if request.method == "POST":
        app = Application.create(user=user, dog=dog)
        dateForm = dateForm(request.POST)
        event = Event(application=app, type="FIRST", title=dog.name + " : " + user.name, start = dateForm.start)
    return redirect(reverse('wad2App:dog'))

@login_required
def showApplication(request, pk):
    user = request.user
    messages = show_messages(request)
    if user.is_staff:
        user = User.objects.get(pk=pk)
    try:
        application = Application.objects.filter(user=user)
    except:
        messages.error(request, 'We could not find that application!')
        return redirect(reverse('wad2App:home'))

    return render(request, 'rango/application.html', {'application' : application, 'messages': messages })

@login_required
def updateApplication(request, pk):
    application = Application.objects.filter(user=user)
    if 'accept' in request.POST:
        application.accepted = True
        application.save()
    elif 'approved' in request.POST:
        application.approved = True
        application.delete()
    return render(request, 'rango/application.html', {'application' : application},)


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

    return (score/len(fields))*100

def calcNewUser(user, dogs, new):
    for dog in dogs:
        score = calc(user, dog)
        if not new:
            dog.scoresField.remove(user)
        dog.scoresField.add(user, through_defaults={'score':score})

######################## MESSAGES ########################
@login_required
def sendMessage(request):
    user = request.user
    if request.method == 'POST':
        if not user.is_staff:
            to = [user for user in User.objects.all() if user.is_staff]
        else:
            to = [User.objects.all()[1]]
        sender = user
        message = MessageForm(request.POST)
        if message.is_valid():
            content = message.cleaned_data['message']
            for user in to:
                Messages.objects.create(sender=sender, to=user, message=content)
    else:
        message = MessageForm()
    return render(request, 'rango/index.html', {'message': message})

@login_required
def show_messages(request):
    context_dict = {}

    inbox = Message.objects.filter(to = user.request)
    sent = Message.objects.filter(receiver = user.request)
    thread = inbox.union(sent).order_by('created_at')

    context_dict["inbox"] = inbox
    context_dict["sent"] = sent
    context_dict["thread"] = thread

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
