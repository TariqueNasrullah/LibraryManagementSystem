from users.views import UserView, UserAdminView, CustomUserCreate
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('profile/', UserView.as_view(), name='profile'),
    path('register/', CustomUserCreate.as_view(), name='registration'),
]

router = DefaultRouter()
router.register(r'users', UserAdminView, basename='users')

urlpatterns += router.urls
