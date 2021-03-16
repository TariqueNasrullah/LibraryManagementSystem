from rest_framework.permissions import BasePermission


class BookLoanCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)


class BookLoanObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.borrower
