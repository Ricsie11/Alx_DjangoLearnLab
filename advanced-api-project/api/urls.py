from django.urls import path
from .views import *

urlpatterns = [
    # Author URLs
    path('authors/', AuthorListView.as_view(), name="author_list"),
    path('authors/create/', AuthorCreateView.as_view(), name="author_create"),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name="author_detail"),
    path('authors/update/<int:pk>/', AuthorUpdateView.as_view(), name="author_update"),
    path('authors/delete/<int:pk>/', AuthorDeleteView.as_view(), name="author_delete"),


    # Book URLs
    path('books/', BookListView.as_view(), name="book_list"),
    path('books/create/', BookCreateView.as_view(), name="book_create"),
    path('books/<int:pk>/', BookDetailView.as_view(), name="book_detail"),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name="book_update"),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name="book_delete"),
]