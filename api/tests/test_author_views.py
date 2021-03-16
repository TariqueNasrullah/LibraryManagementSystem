from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status
from users.serializers import CustomUserSerializer
from api.models import Author
from api.serializers import AuthorSerializer


class TestAuthorViews(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(email="admin@admin.com", username="admin",
                                                        first_name="Mighty", last_name="Hulk", password="pass")

        self.author = Author.objects.create(name="Kazi Nazrul", country="BD", occupation="Novelist", education="SSC",
                                            biography="Biography details")

        # Attempt to get personal profile with authenticated user
        resp = self.client.post(reverse('token_obtain_pair'),
                                {'email': 'admin@admin.com', 'password': 'pass'}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg="Unexpected response code")

        self.assertTrue('access' in resp.data)
        self.assertTrue('refresh' in resp.data)

        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + resp.data['access'])

        self.authorizedClient = client

    def test_create_author(self):
        resp = self.authorizedClient.post(reverse('api:authors-list'),
                                          {"name": "Kazi Nazrul", "country": "BD", "occupation": "Novelist",
                                           "education": "School", "biography": "bio graphy about kazinazrul"},
                                          format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        created_author = Author.objects.get(pk=resp.data['id'])
        serializer = AuthorSerializer(created_author)

        self.assertEqual(resp.data, serializer.data)

    def test_get_authors(self):
        resp = self.authorizedClient.get(reverse('api:authors-list'), format='json')

        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)

        self.assertEqual(resp.data['results'], serializer.data)

    def test_update_author(self):
        # Attempt to modify name of author
        new_name = "Kazi Nazrul Islam"
        resp = self.authorizedClient.patch(reverse('api:authors-detail', kwargs={'pk': self.author.id}),
                                           {"name": new_name}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.author = Author.objects.get(pk=self.author.id)
        serializer = AuthorSerializer(self.author)

        self.assertEqual(resp.data, serializer.data)

    def test_delete_author(self):
        # Attempt to delete Author
        resp = self.authorizedClient.delete(reverse('api:authors-detail', kwargs={'pk': self.author.id}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)