from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

# Create your views here.

@permission_required("bookshelf.can_create", raise_exception=True)  # With the permission_required decorator and raise exception
@permission_required("bookshelf.can_edit", raise_exception=True)    # users who are already logged in and has one of this permissions missing would just get a 403 error message instead of
@permission_required("bookshelf.can_delete", raise_exception=True)  # of just being taken to the login page

def manage_book(request):
    return HttpResponse ("You are allowed to edit, delete and create Books")