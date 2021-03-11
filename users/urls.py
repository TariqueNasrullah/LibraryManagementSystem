from django.urls import path
from .views import UserList

app_name = 'users'

urlpatterns = [
    path('test-get/', UserList.as_view(), name="user_list"),
]