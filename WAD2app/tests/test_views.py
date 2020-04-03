from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from . import factories
import factory
import unittest


class SignInTest(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()


    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = self.user
        response = self.client.post('/signin/', {'username': user.username, 'password': user.password})
        self.assertTrue(response.data['authenticated'])

    def test_wrong_username(self):
        user = self.user
        response = self.client.post('/signin/', {'username': 'wrong', 'password': user.password})
        self.assertFalse(response.data['authenticated'])

    def test_wrong_pssword(self):
        user = self.user
        response = self.client.post('/signin/', {'username': user.username, 'password': 'wrong'})
        self.assertFalse(response.data['authenticated'])
