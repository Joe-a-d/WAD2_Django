from django.contrib.auth.models import User
from django.test import TestCase

class SignInTest(TestCase):

    user = factories.UserFactory(username='james', password='password123')

    def test_correct(self):
        user = authenticate(username='james', password='password123')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='james', password='password123')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='james', password='asd')
        self.assertFalse(user is not None and user.is_authenticated)

    def test(self):
        self.assertTrue(True,False)

class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
