from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Member, Profile, Project
import factory
from . import factories

class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()

        # Normal user
        self.notStaff = factories.UserFactory(is_staff=False)
        self.notStaff.set_password("pswd")
        self.notStaff.save()

        # Staff

        self.staff = factories.UserFactory(is_staff=True)
        self.staff.set_password("pswd")
        self.staff.save()

        # Dog with favourites and pending application
        self.dog = factories.DogFactory(favourites=self.notStaff, is_reserved=True)

        # Dog with invalid favourite
        self.staffDog = factories.DogFactory(favourites=self.staff)
