#Query all books by a specific author.
books = Book.objects.filter(author=author)

#List all books in a library.
books = library.books.all()
Library.objects.get(name=library_name)

#Retrieve the librarian for a library.
librarian = library.librarian