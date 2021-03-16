from django.contrib import admin
from api.models import Book, Author, BookLoan

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(BookLoan)