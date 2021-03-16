import django_filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS
from api.permissions import BookLoanCreatePermission, BookLoanObjectOwner
from api.serializers import BookSerializer, AuthorSerializer, BookLoanSerializer, BookLoanCreateRequestSerializer
from api.models import Book, Author, BookLoan
from rest_framework import viewsets
from api.utils import StandardResultsSetPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['authors']

    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Author.objects.all()


class BookLoanViewSet(viewsets.ModelViewSet):
    serializer_class = BookLoanSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['borrower']

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return BookLoan.objects.all()
            else:
                return BookLoan.objects.filter(borrower=self.request.user)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['create']:
            permission_classes = [IsAuthenticated & BookLoanCreatePermission]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated & (IsAdminUser | BookLoanObjectOwner)]
        elif self.action in ['put', 'patch', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create']:
            return BookLoanCreateRequestSerializer
        return BookLoanSerializer

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
