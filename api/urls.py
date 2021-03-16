from api.views import BookViewSet, AuthorViewSet, BookLoanViewSet

from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'loans', BookLoanViewSet, basename='loans')

urlpatterns = router.urls
