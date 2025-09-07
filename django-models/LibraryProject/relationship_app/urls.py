from django.urls import path
from .views import list_books , LibraryDetailView
from . import views


urlpatterns = [
    path('books/', list_books, name="list_books"),
    path('library/<int:pk>/', LibraryDetailView.as_view, name="library_detail"),
    path('login/', LoginView.as_view(template_name="login")),
    path('register/', views.register_view(template_name="register")),
    path('logout/', LogoutView.as_view(template_name="logout")),
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/edit/<int:book_id>/", views.edit_book, name="edit_book"),
    path("books/delete/<int:book_id>/", views.delete_book, name="delete_book"),
]


urlpatterns = [
    # Book permission-based views
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:book_id>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:book_id>/", views.delete_book, name="delete_book"),
]
