from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Author, Book
from api.serializers import BookSerializer
from users.models import CustomUser


client = APIClient()


class AuthenticationTest(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(email='admin@admin.com', username='admin',
                                                         first_name='admin', password='admin')

    def test_api_jwt(self):
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'admin@admin.com', 'password': 'admin'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg="Unexpected response code")
        self.assertTrue('access' in resp.data)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + resp.data['access'])


class AuthorTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Alice', country='US', occupation='novelist',
                                            education='MIT', biography='alice is a fine novelist')

    # def test_author_fields(self):
    #
    #     response = client.get(reverse('api:books-list'), format='json')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Unexpected response code")
    #
    #     books = Book.objects.all()
    #     serializer = BookSerializer(books, many=True)
    #
    #     self.assertEqual(response.data['results'], serializer.data)