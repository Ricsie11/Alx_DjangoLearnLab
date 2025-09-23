from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
     # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name="book-list"), #Maps to the BookList view

      # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)), # This includes all routes registered with the router

    path('api/token/', obtain_auth_token, name='obtain_token'),  # Endpoint for obtaining auth token
]