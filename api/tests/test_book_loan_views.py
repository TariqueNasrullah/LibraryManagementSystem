from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status
from users.serializers import CustomUserSerializer
from api.models import Author, Book, BookLoan
from api.serializers import AuthorSerializer, BookSerializer, BookLoanSerializer
from rest_framework_simplejwt import tokens


class TestBookLoanViews(TestCase):
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

        self.adminUser = CustomUser.objects.create_superuser(email="admin@admin.com", username="admin",
                                                             first_name="Mighty", last_name="Hulk", password="pass")
        self.user = CustomUser.objects.create_user(email="user@user.com", username="user",
                                                   first_name="Bob", last_name="Alice", password="pass")

        self.loan1 = BookLoan.objects.create(book_id=self.book1.id, borrower=self.user)
        self.loan1 = BookLoan.objects.create(book_id=self.book2.id, borrower=self.user)

        token = tokens.AccessToken.for_user(self.adminUser)

        admin_client = APIClient()
        admin_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.__str__())

        self.authorizedClient = admin_client


        token = tokens.AccessToken.for_user(self.user)
        user_client = APIClient()
        user_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.__str__())
        self.userClient = user_client

    def test_request_book_loan(self):
        resp = self.userClient.post(reverse('api:loans-list'),
                                    {'book': self.book1.id}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_get_own_book_loan_list(self):
        resp = self.userClient.get(reverse('api:loans-list'), format='json')

        loans = BookLoan.objects.filter(borrower=self.user)
        serializer = BookLoanSerializer(loans, many=True)
        self.assertEqual(resp.data, serializer.data)

    def test_get_book_loan_list_by_admin(self):
        resp = self.authorizedClient.get(reverse('api:loans-list'), format='json')

        loans = BookLoan.objects.all()
        serializer = BookLoanSerializer(loans, many=True)
        self.assertEqual(resp.data, serializer.data)

    def approve_book_loan_by_admin(self):
        resp = self.authorizedClient.post(reverse('api:loans-detail', kwargs={'pk': self.loan1.id}),
                                          {'status': 'APPROVED'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def decline_book_loan_by_admin(self):
        resp = self.authorizedClient.post(reverse('api:loans-detail', kwargs={'pk': self.loan2.id}),
                                          {'status': 'REJECTED'}, format='json')
