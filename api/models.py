from django.db import models
from users.models import CustomUser


class Author(models.Model):
    name = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True, null=False)
    title = models.CharField(max_length=250, null=False)
    length = models.IntegerField(default=0)
    date_of_publication = models.DateField(null=False)
    publisher = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='images', blank=True)
    authors = models.ManyToManyField(to=Author, related_name='authors', blank=False)

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, blank=False)
    borrower = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('RETURNED', 'Returned'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.book.title + " | " + self.borrower.username
