from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})



# Class-based view for library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


#registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Logs in the user automatically
            messages.success(request, "Registration Successful!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {'form':form})


#login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "logged in successful!")
                return redirect ("home")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {'form':form})


#logout view
def logout_view(request):
    logout (request)
    messages.info((request, "You have successfully logged out!"))
    return render(request, "relationship_app/logout.html")
