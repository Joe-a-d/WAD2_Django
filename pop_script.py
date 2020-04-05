import os,sys, importlib, inspect,django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD2.settings')
django.setup()
from factories import *


#
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
#         print(f"{obj}")


def pop():
        # UserFactory.create_batch(size=50, username=factory.Sequence(lambda n: 'username{0}'.format(n)))
        #ProfileFactory()
        # PrefFactory.create_batch(size=1)
        # LifeFactory.create_batch(size=1)
        # DogFactory.create_batch(size=50)
         ApplicationFactory.create_batch(size=1)
        # EventFactory.create_batch(size=1)
        # ScoresFactory.create_batch(size=1)
        # MessageFactory.create_batch(size=1)
        # ProfileFactory.create_batch(size=1)

pop()
