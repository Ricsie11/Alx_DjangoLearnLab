from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .forms import SearchForm
from .models import Book
from.forms import ExampleForm  


# Create your views here.

@permission_required("bookshelf.can_create", raise_exception=True)  # With the permission_required decorator and raise exception
@permission_required("bookshelf.can_edit", raise_exception=True)    # users who are already logged in and has one of this permissions missing would just get a 403 error message instead of
@permission_required("bookshelf.can_delete", raise_exception=True)  # of just being taken to the login page

def book_list(request):
    return HttpResponse ("You are allowed to edit, delete and create Books")


def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the data here
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # You could save it, send an email, etc.
            return redirect('success')  # Replace with your success URL
    else:
        form = ExampleForm()
    return render(request, 'example_form.html', {'form': form})


