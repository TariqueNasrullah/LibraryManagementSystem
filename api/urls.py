from django.urls import path
from api.views import BookViewSet, AuthorViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'authors', AuthorViewSet, basename='authors')

app_name = 'api'

urlpatterns = router.urls
