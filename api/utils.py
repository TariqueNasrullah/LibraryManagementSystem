from rest_framework import pagination


class StandardResultsSetPagination(pagination.LimitOffsetPagination):
    default_limit = 50
