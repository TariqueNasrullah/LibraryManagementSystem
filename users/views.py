import django_filters
from rest_framework import viewsets
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status


class CustomUserCreate(APIView):
    """
    ApiView that supports only POST request, creates an user
    Used for user registration.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    """
    UserView ApiView that supports GET, PATCH request .Used
    it for getting own profile of the user and update profile
    information.
    PATCH supports partial update of the fields
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request):
        profile = self.get_object(pk=request.user.id)
        serializer = CustomUserSerializer(profile)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request):
        profile = self.get_object(pk=request.user.id)
        serializer = CustomUserSerializer(profile, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserAdminView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id', 'email', 'username']
    search_fields = ['username', 'email']
