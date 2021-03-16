from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status
from users.serializers import CustomUserSerializer
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from rest_framework_simplejwt import tokens


class TestBookViews(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='Author_Name_1')
        self.author2 = Author.objects.create(name='Author_Name_2')
        self.author3 = Author.objects.create(name='Author_Name_3')

        self.book1 = Book.objects.create(isbn='isbn1', title='Book_title_1', date_of_publication='1997-1-12')
        self.book1.authors.add(self.author1)
        self.book1.authors.add(self.author2)
        self.book1.save()

        self.book2 = Book.objects.create(isbn='isbn2', title='Book_title_1', date_of_publication='1997-1-11')
        self.book2.authors.add(self.author2)
        self.book2.authors.add(self.author3)
        self.book2.save()

        self.user = CustomUser.objects.create_superuser(email="admin@admin.com", username="admin",
                                                        first_name="Mighty", last_name="Hulk", password="pass")

        token = tokens.AccessToken.for_user(self.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.__str__())

        self.authorizedClient = client

    def test_get_books(self):
        resp = self.authorizedClient.get(reverse('api:books-list'), format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(resp.data['results'], serializer.data)

    def test_create_book(self):
        resp = self.authorizedClient.post(reverse('api:books-list'),
                                          {"title": "A new Book", "isbn": "isbn123",
                                           "date_of_publication": "2021-03-10",
                                           "author_ids": [2]}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        created_book = Book.objects.get(pk=resp.data['id'])
        serializer = BookSerializer(created_book)

        self.assertEqual(resp.data, serializer.data)

    def test_update_book(self):
        # Attempt to update book information
        resp = self.authorizedClient.patch(reverse('api:books-detail', kwargs={'pk': self.book1.id}),
                                           {'title': 'Edited Title', "author_ids": [self.author1.id]}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.book1 = Book.objects.get(pk=self.book1.id)
        serializer = BookSerializer(self.book1)

        self.assertEqual(resp.data, serializer.data)

    def test_delete_book(self):
        # Attempt to delete Book
        resp = self.authorizedClient.delete(reverse('api:books-detail', kwargs={'pk': self.book1.id}), format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
