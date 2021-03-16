from rest_framework import serializers
from api.models import Book, Author, BookLoan
from users.serializers import CustomUserSerializer
from django.utils import timezone

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all(), write_only=True)

    class Meta:
        model = Book
        fields = ('id', 'isbn', 'title', 'cover_image', 'date_of_publication', 'authors', 'author_ids')
        extra_kwargs = {'authors_ids': {'write_only': True}}
        depth = 1

    def create(self, validated_data):
        authors = validated_data.pop('author_ids', [])
        obj = Book.objects.create(**validated_data)
        obj.authors.set(authors)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        authors = validated_data.pop('author_ids', [])
        instance = super(BookSerializer, self).update(instance, validated_data)
        instance.authors.set(authors)

        return instance


class BookLoanSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        updated_status = validated_data.pop('status', instance.status)

        instance = super(BookLoanSerializer, self).update(instance, validated_data)

        if instance.status != updated_status:
            if updated_status == 'APPROVED':
                instance.due_date = timezone.now().date() + timezone.timedelta(days=14)
            elif updated_status == 'RETURNED':
                instance.returned_date = timezone.now().date()

            instance.status = updated_status
            instance.save()

        return instance


class BookLoanCreateRequestSerializer(serializers.ModelSerializer):
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