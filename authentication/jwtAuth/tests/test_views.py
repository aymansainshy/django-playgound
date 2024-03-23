from .test_setup import TestSetup
from ..models import User


class TestView(TestSetup):

    def test_user_can_not_register_with_no_data(self):
        response = self.client.post(self.register_url)
        # expect to get this response
        self.assertEqual(response.status_code, 400)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data, format='json')

        # expect to get this response
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.status_code, 201)

    def test_user_can_not_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.user_data, format='json')

        self.assertEqual(response.status_code, 401)

    def test_user_can_login_after_verified_email(self):
        res = self.client.post(self.register_url, self.user_data, format='json')
        email = res.data['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()

        response = self.client.post(self.login_url, self.user_data, format='json')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, 200)
