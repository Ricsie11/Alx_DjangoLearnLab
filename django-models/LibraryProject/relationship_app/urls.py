from django.urls import path
from .views import *

urlpatterns = [
    path('books/', list_books, name="list_books"),
    path('library/<int:pk>/', LibraryDetailView.as_view, name="library_detail"),

]