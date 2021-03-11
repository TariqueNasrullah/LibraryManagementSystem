from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from django.http import Http404


class UserList(APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404('User not found')

    def get(self, request):
        user = self.get_object(1)
        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
