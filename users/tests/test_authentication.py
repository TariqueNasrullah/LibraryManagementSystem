from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status
from users.serializers import CustomUserSerializer


class AuthenticationTest(TestCase):
    def setUp(self):
        self.apiClient = APIClient()

        # Create a Super User Account
        self.adminUser = CustomUser.objects.create_superuser(email="admin@admin.com", username="admin",
                                                             first_name="Tony", last_name="Stark", password="admin")

        self.user = CustomUser.objects.create_user(email="user@user.com", username="user",
                                                   first_name="Bob", last_name="Daylan", password="user")

    def test_registration_api(self):
        # Attempt to register without password
        # This should raise 404 Bad Request
        resp = self.client.post(reverse('users:registration'),
                                {"email": "a@a.com", "username": "leo", "first_name": "leonel", "last_name": "messi"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Registration valid request
        resp = self.client.post(reverse('users:registration'),
                                {"email": "a@a.com", "username": "leo", "first_name": "leonel",
                                 "last_name": "messi", "password": "SuperSecretPassword"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_login_with_jwt_api(self):
        # Attempt to get token with invalid password, Expected 401 Unauthorized respnse code
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'user@user.com', 'password': 'invalid_pass'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, msg="Unexpected response code")

        # Attempt to get token with invalid email, Expected 401 Unauthorized respnse code
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'b@b.com', 'password': 'user'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, msg="Unexpected response code")

        # Attempt to get token with valid email and password, Expected 401 Unauthorized respnse code
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'user@user.com', 'password': 'user'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg="Unexpected response code")

        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)
