import os,sys, importlib, inspect,django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2.settings')
django.setup()
from factories import *


# terribly hacky pop all vs args, -10pt to grifindor

models = sys.argv
n = int(models[1])
models = models[2:]
if not models:
    UserFactory.create_batch(size=n, username=factory.Sequence(lambda n: 'username{0}'.format(n)), password="pwd")
    ProfileFactory.create_batch(size=n)
    PrefFactory.create_batch(size=n)
    LifeFactory.create_batch(size=n)
    DogFactory.create_batch(size=n)
    ApplicationFactory.create_batch(size=n)
    EventFactory.create_batch(size=n)
    ScoresFactory.create_batch(size=n)
    MessageFactory.create_batch(size=n)
if 'user' in models:
    UserFactory.create_batch(size=n, username=factory.Sequence(lambda n: 'username{0}'.format(n)), password="pwd")

if 'profile' in models:
    ProfileFactory.create_batch(size=n)

if 'preferences' in models:
    PrefFactory.create_batch(size=n)

if 'life' in models:
    LifeFactory.create_batch(size=n)

if 'dog' in models:
    DogFactory.create_batch(size=n)

if 'app' in models:
    ApplicationFactory.create_batch(size=n)

if 'event' in models:
    EventFactory.create_batch(size=n)

if 'scores' in models:
    ScoresFactory.create_batch(size=n)

if 'messages' in models:
    MessageFactory.create_batch(size=n)




# TODO: Feature
# classes = []
#
# for name, obj in inspect.getmembers(sys.modules[__name__]):
#         if inspect.isclass(obj):
#             classes.append(obj)
#
#
# for c in classes:
#     try:
#         factories.c.create_batch(size=50)
#     except:
#
