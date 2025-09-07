#Query all books by a specific author.
books = Book.objects.filter(author=author)

#List all books in a library.
books = library.objects.all()

#Retrieve the librarian for a library.
librarian = library.librarian