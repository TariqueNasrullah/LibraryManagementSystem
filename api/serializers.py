from rest_framework import serializers
from api.models import Book, Author, BookLoan
from users.serializers import CustomUserSerializer
from django.utils import timezone


class AuthorSerializer(serializers.ModelSerializer):
    """
    Basic Serializer for Author Model
    """

    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book Model.
    """

    # author_ids, list of Author IDs, that is used
    # to assign relation between Book and Authors
    author_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all(), write_only=True)

    class Meta:
        model = Book
        fields = ('id', 'isbn', 'title', 'cover_image', 'date_of_publication', 'authors', 'author_ids')
        extra_kwargs = {'authors_ids': {'write_only': True}}  # write only fields, that won't appear in the request
        depth = 1  # Allow Author Details to be in the same response

    # create overrides ModelSerializer's create method
    def create(self, validated_data):
        # extract author ids from the request
        authors = validated_data.pop('author_ids', [])

        # Create a new book instance
        obj = Book.objects.create(**validated_data)

        # Set Authors to the book
        obj.authors.set(authors)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        # extract author ids from the request
        authors = validated_data.pop('author_ids', [])

        # update the book instance
        instance = super(BookSerializer, self).update(instance, validated_data)

        # set authors to the book
        instance.authors.set(authors)

        return instance


class BookLoanSerializer(serializers.ModelSerializer):
    """
    BookLoanSerializer for BookLoan Model, that expose the status field to be changed
    """
    borrower = CustomUserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = BookLoan
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'due_date': {'read_only': True},
            'returned_date': {'read_only': True},
            'borrower': {'read_only': True},
            'book': {'read_only': True},
        }

    # Override update method to allow validation check on loan status change
    def update(self, instance, validated_data):
        # Extract STATUS from the request
        updated_status = validated_data.pop('status', instance.status)

        # Update the instance without status change
        instance = super(BookLoanSerializer, self).update(instance, validated_data)

        # Validation for status Changes
        if instance.status != updated_status:
            if updated_status == 'APPROVED':
                instance.due_date = timezone.now().date() + timezone.timedelta(days=14)
            elif updated_status == 'RETURNED':
                instance.returned_date = timezone.now().date()

            instance.status = updated_status
            instance.save()

        return instance


class BookLoanCreateRequestSerializer(serializers.ModelSerializer):
    """
    BookLoanCreateRequestSerializer serializes book loan request,
    restricts user to pass status field in the request. Default
    status of a loan is 'PENDING'
    """
    borrower = CustomUserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = BookLoan
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'due_date': {'read_only': True},
            'returned_date': {'read_only': True},
            'borrower': {'read_only': True},
            'status': {'read_only': True},
        }
