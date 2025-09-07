from django.urls import path
from .views import list_books , LibraryDetailView
from . import views

urlpatterns = [
    path('books/', list_books, name="list_books"),
    path('library/<int:pk>/', LibraryDetailView.as_view, name="library_detail"),
    path('login/', LoginView.as_view(template_name="login")),
    path('register/', views.register_view(template_name="register")),
    path('logout/', LogoutView.as_view(template_name="logout")),

]