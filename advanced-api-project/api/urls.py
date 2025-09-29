from django.urls import path
from .views import *

urlpatterns = [
    # Author URLs
    path('author/', AuthorListView.as_view(), name="author_list"),
    path('author/create/', AuthorCreateView.as_view(), name="author_create"),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name="author_detail"),
    path('author/<int:pk>/update/', AuthorUpdateView.as_view(), name="author_update"),
    path('author/<int:pk>/destroy/', AuthorDestroyView.as_view(), name="author_destroy"),


    # Book URLs
    path('book/', BookListView.as_view(), name="book_list"),
    path('book/create/', BookCreateView.as_view(), name="book_create"),
    path('book/<int:pk>/', BookDetailView.as_view(), name="book_detail"),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name="book_update"),
    path('book/<int:pk>/destroy/', BookDestroyView.as_view(), name="book_destroy"),
]