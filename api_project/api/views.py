from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] #Only logged in user can access

    def get_queryset(self):
        #Only show books for the logged in user
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        #Automatically assign the logged-in user to the book
        serializer.save(user=self.request.user)
