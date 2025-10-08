from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('Register/', RegisterView.as_view(), name="register"),
    path('Login/', LoginView.as_view(), name="Login"),
]