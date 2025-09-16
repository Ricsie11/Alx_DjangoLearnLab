from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .forms import SearchForm
from .models import Book

# Create your views here.

@permission_required("bookshelf.can_create", raise_exception=True)  # With the permission_required decorator and raise exception
@permission_required("bookshelf.can_edit", raise_exception=True)    # users who are already logged in and has one of this permissions missing would just get a 403 error message instead of
@permission_required("bookshelf.can_delete", raise_exception=True)  # of just being taken to the login page

def book_list(request):
    return HttpResponse ("You are allowed to edit, delete and create Books")


def search_view(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        results = Book.objects.filter(name__icontains=query)
    return render(request, 'search.html', {'form': form, 'results': results})

