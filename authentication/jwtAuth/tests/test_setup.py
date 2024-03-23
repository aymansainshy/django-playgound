from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),  # 'user@gmail.com',
            'username': self.fake.email().split('@')[0],  # 'username',
            'password': self.fake.email()  # 'password'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
