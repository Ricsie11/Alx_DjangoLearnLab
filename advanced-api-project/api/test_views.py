from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author

# Test Class for Book API
class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # Log the user in
        self.client.login(username='testuser', password='testpass')

        # Create test author and book
        self.author = Author.objects.create(name='J.K. Rowling')
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            author=self.author,
            publication_year=1997
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            author=self.author,
            publication_year=1998
        )

        self.book_list_url = reverse('book-list')  # 'book-list' must match your URL name

#Test Cases
    def test_get_books_list(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


#Test: Create a new book
    def test_create_book(self):
        data = {
            'title': 'Fantastic Beasts',
            'author': self.author.id,
            'publication_year': 2001
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

#Test: Update a book
    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Harry Potter and the Sorcerer\'s Stone',
            'author': self.author.id,
            'publication_year': 1997
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Sorcerer\'s Stone')

#Test: Delete a book
    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)


#Test: Search by title
    def test_search_books_by_title(self):
        response = self.client.get(self.book_list_url + '?search=Chamber')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Chamber of Secrets')


#Test: Filter by publication_year
    def test_filter_books_by_publication_year(self):
        response = self.client.get(self.book_list_url + '?publication_year=1997')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1997)


#Test: Ordering
    def test_order_books_by_title_desc(self):
        response = self.client.get(self.book_list_url + '?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')


#
