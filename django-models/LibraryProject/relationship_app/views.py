from django.shortcuts import render
from django.views.generic import DetailView
from .models import *

# Create your views here.

def list_books(request):
    books = Book.objects.all()
    output = ""
  

    for book in books:
        output += f"{book.title} by {book.author.name}"
    

    return render(output)


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["books"] = self.objects.book.all() #fetch books for this library
        return context
