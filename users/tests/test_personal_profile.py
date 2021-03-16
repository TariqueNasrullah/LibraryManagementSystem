from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status
from users.serializers import CustomUserSerializer


class PersonalProfileApiTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="user@user.com", username="user",
                                                   first_name="Bob", last_name="Daylan", password="pass")

        # Attempt to get personal profile with authenticated user
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'user@user.com', 'password': 'pass'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg="Unexpected response code")

        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + resp.data['access'])

        self.authorizedClient = client

    def test_get_personal_profile(self):
        # Attempt to get personal profile with unauthenticated user
        resp = self.client.get(reverse('users:profile'))
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # Attempt to get personal profile with authenticated user
        resp = self.authorizedClient.get(reverse('users:profile'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        serializer = CustomUserSerializer(self.user)
        self.assertEqual(resp.data, serializer.data)

    def test_edit_personal_profile(self):
        # Attempt to edit first name, Set to Alice
        resp = self.authorizedClient.patch(reverse('users:profile'),
                                           {'first_name': 'Alice'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(self.user.first_name, 'Alice')
