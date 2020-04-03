import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2.settings')

import django
django.setup()
from WAD2app.models import *

def populate():

    dogs : [
       {'name': 'Abu,(female golden pup)',
        'size': 'L',
        'age': 'PUP',
        'gender': 'F',
        'energy': 'H',
        'breed': 'Golden retriever',
        'houseTrained': 'True',
        'isAvailable': 'True',},
       {'name': 'Billy, (female bull 1-2)',
        'size': 'S',
        'age': '2',
        'gender': 'F',
        'energy': 'H',
        'breed': 'Bulldog',
        'houseTrained': 'True',
        'isAvailable' : 'True',},
       {'name': 'Jimmy, (male golden 2-5)',
        'size': 'L',
        'age': '3',
        'gender': 'M',
        'energy': 'H',
        'breed': 'Golden retriever',
        'houseTrained': 'Flase',
        'isAvailable' : 'True',},
       {'name': 'Gale, (female golden 5+)',
        'size': 'L',
        'age': '4',
        'gender': 'F',
        'energy': 'M',
        'breed': 'Golden retriever',
        'houseTrained': 'True',
        'isReserved' : 'True',}, ]
    users : [
        {'username': 'Alexis',
         'password': '123456',
         'email': '1@gmail.com'},
        {'username': 'John',
         'password': '000000',
         'email': '2@gmail.com'},
        {'username': 'Leonardo',
         'password': '654321',
         'email': '3@gmail.com'}]
    userProfiles : [
        {'postcode': 'G3 1QS',
         'building': 5,
         'address': 'whatever',
         'phone': 07412345678,},
        {'postcode': 'G4 1MS',
         'building': 100,
         'address': 'whatever',
         'phone': 07443215678,},
        {'postcode': 'G11 1SS',
         'building': 7,
         'address': 'whatever',
         'phone': 07412345078,},]
    userPrefs : [
        {'breed': 'golden retriever',
         'size': 'L',
         'age': 'PUP',
         'gender': 'F'},
        {'breed': 'golden retriever',
         'size': 'L',
         'age': 'PUP',
         'gender': 'M'
         'houseTrained': 'True',
         'energyLevel': 'H'},
        {'breed': 'Huski',
         'size': 'L',
         'age': '2',
         'gender': 'M'
         'houseTrained': 'True',
         'energyLevel': 'H'}]
    userLifes : [
        {'lifestyle':'H',
         'timeAway': 8,
         'house': 'APT',
         'garden': False,
         'hasCat': False,
         'hasDog': False,
         'cohab': 1,
         'hasChildren': False,
         'trainer': False,
         'dogOwner': False},
        {'lifestyle':'M',
         'timeAway': 8,
         'house': 'HO',
         'garden': True,
         'hasCat': False,
         'hasDog': False,
         'cohab': 4,
         'hasChildren': True,
         'trainer': False,
         'dogOwner': False},]

        for dog in dogs:
        add_dog (name:dog['name'], size:dog['size'], age:dog['age'],
                 gender:dog['gender'], energy:dog['energy'], breed:dog['breed'],
                 houseTrained:dog['houseTrained'],
                 isAvailable:dog['isAvailable'],
                 isReserved:dog['isReserved'])
        for i in range len(users):
            user : User.objects.create_user(username:users[i]['username'],
                                 email:users[i]['email'],
                                 password:users[i]['password'])
            add_userProfile (user, postcode:userProfiles[i]['postcode'],
                             building:userProfiles[i]['building'],
                             address:userProfiles[i]['address'],
                             phone:userProfiles[i]['phone'])
            add_userPref (user, breed:userPrefs[i]['breed'],
                          size:userPrefs[i]['size'], age:userPrefs[i]['age'],
                          gender:userPrefs[i]['gender'],
                          houseTrained:userPrefs[i]['houseTrained'],
                          energyLevel:userPrefs[i]['energyLevel'])

def add_dog (name, size, age, gender, energy, breed, houseTrained:False,
             isAvailable:True, isReserved:False):
        d : Dog.objects.create_Dog()
        d.name : name
        d.size : size
        d.age : age
        d.gender : gender
        d.energy : energy
        d.breed : breed
        d.houseTrained : houseTrained
        d.isAvailable : isAvailable
        d.isReserved : isReserved
        d.save()
        return d

def add_userProfile (User, postcode, building, address, phone):
        p : UserProfile.objects.create_UserProfile()
        p.user : User
        p.postcode : postcode
        p.building : building
        p.address : address
        p.phone : phone
        p.save()
        return p

def add_userPref (User, breed, size, age, gender, houseTrained, energyLevel):
        p : UserPref.objects.create_UserPref()
        p.user : User
        p.size : size
        p.age : age
        p.gender : gender
        p.energyLevel : energyLevel
        p.breed : breed
        p.houseTrained : houseTrained
        p.save()
        return p
         
        
