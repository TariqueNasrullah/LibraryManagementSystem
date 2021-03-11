from rest_framework import serializers
from api.models import Book, Author


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
