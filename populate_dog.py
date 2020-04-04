import os
from WAD2.wsgi import *

def populate():

    dogs = (
        {"name": "Chalie",
            "size": "L",
            "age": "PUP",
            "gender": "F",
            "energy": "H",
            "breed": "Golden retriever",
            "houseTrained": True,
            "isReserved" : False,
            "isAvailable": True,},
       {"name": "Molly",
        "size": "S",
        "age": "2",
        "gender": "F",
        "energy": "H",
        "breed": "Bulldog",
        "houseTrained": True,
        "isReserved" : False,
        "isAvailable" : True,},
       {"name": "Ruby",
        "size": "L",
        "age": "3",
        "gender": "M",
        "energy": "H",
        "breed": "Golden retriever",
        "houseTrained": False,
        "isReserved" : False,
        "isAvailable" : True,},
       {"name": "Buddy",
        "size": "L",
        "age": "4",
        "gender": "F",
        "energy": "M",
        "breed": "Golden retriever",
        "houseTrained": True,
        "isReserved" : True,
        "isAvailable" : False,},)

    for dog in dogs:
        add_dog (dog['name'], dog['size'], dog['age'],
                dog['gender'], dog['energy'], dog['breed'],
                dog['houseTrained'],
                dog['isAvailable'],
                dog['isReserved'])

def add_dog (name, size, age, gender, energy, breed, houseTrained:False,
             isAvailable:True, isReserved:False):
        d = Dog.objects.get_or_create(
        name = name,
        size = size,
        age = age,
        gender = gender,
        energyLevel = energy,
        breed = breed,
        houseTrained = houseTrained,
        isAvailable = isAvailable,
        isReserved = isReserved,
        )[0]
        return d
         
if __name__ == '__main__':
    print("Populating...")
    from WAD2app.models import Dog
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2.settings')
    populate()
    print("Population complete!")