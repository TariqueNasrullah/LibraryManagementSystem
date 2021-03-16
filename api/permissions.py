from rest_framework.permissions import BasePermission


class BookLoanCreatePermission(BasePermission):
    """
    BookLoanCreatePermission allows unprivileged authenticated user
    to request for a book loan. Admin is not allowed to create new
    loan request.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)


class BookLoanObjectOwner(BasePermission):
    """
    Object level permission for BookLoan object, User is able to Cancel or delete
    Loan request if its not yet approved or rejected
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.borrower
