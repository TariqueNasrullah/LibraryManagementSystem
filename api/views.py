import django_filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.permissions import BookLoanCreatePermission, BookLoanObjectOwner
from api.serializers import BookSerializer, AuthorSerializer, BookLoanSerializer, BookLoanCreateRequestSerializer
from api.models import Book, Author, BookLoan
from rest_framework import viewsets
from api.utils import StandardResultsSetPagination


class BookViewSet(viewsets.ModelViewSet):
    """
    BookViewSet allows GET, POST, PUT, PATCH, DELETE request for Book Model
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # setup filter backend
    filterset_fields = ['authors']  # allow filter by authors

    pagination_class = StandardResultsSetPagination  # default pagination

    def get_permissions(self):
        """
        Override get_permissions method, for custom permission
        Admin is allowed to create, update and delete books.
        Unprivileged users allowed to query books.
        :return: Permission
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class AuthorViewSet(viewsets.ModelViewSet):
    """
    AuthorViewSet allows GET, POST, PUT, PATCH, DELETE request for Book Model
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # setup filter backend
    filterset_fields = ['name']  # allow filter by name

    pagination_class = StandardResultsSetPagination  # default pagination

    def get_permissions(self):
        """
        Override get_permissions method, for custom permission
        Admin is allowed to create, update and delete authors.
        Unprivileged users allowed to query authors.
        :return: Permission
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class BookLoanViewSet(viewsets.ModelViewSet):
    serializer_class = BookLoanSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # setup filter backend
    filterset_fields = ['borrower'] # allow filter by borrower

    def get_queryset(self):
        """
        Override get_queryset method to apply object level permission of the BookLoan Objects.
        Unprivileged user is not allowed to query other's loan details
        :return: QuerySet
        """
        if self.request.user and self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return BookLoan.objects.all()
            else:
                return BookLoan.objects.filter(borrower=self.request.user)

    def get_permissions(self):
        """
        Override get_permissions for custom permission, only User is allowed to request for loan.
        Admin can access all loan data and modify them.
        :return: Permission
        """
        permission_classes = [IsAuthenticated]

        if self.action in ['create']:
            permission_classes = [IsAuthenticated & BookLoanCreatePermission]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated & (IsAdminUser | BookLoanObjectOwner)]
        elif self.action in ['put', 'patch', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Sets up dynamic serializer class. BookLoanCreateRequestSerializer is for post request.
        BookLoanSerializer applies otherwise
        :return:
        """
        if self.action in ['create']:
            return BookLoanCreateRequestSerializer
        return BookLoanSerializer

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
