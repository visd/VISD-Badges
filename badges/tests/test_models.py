from django.test import TestCase

from django.contrib.auth.models import User, Group

from badges import models
from build.factories import UserFactory

class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()