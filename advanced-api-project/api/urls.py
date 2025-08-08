from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    # Retrieve a single book by ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    # Create a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    # Update books (bulk or custom endpoint)
    path('books/update/', BookUpdateView.as_view(), name='books-update'),
    # Delete books (bulk or custom endpoint)
    path('books/delete/', BookDeleteView.as_view(), name='books-delete'),
    # Update an existing book (PUT/PATCH)
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    # Delete a book (DELETE)
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]

# Documentation:
# - /books/ : GET for list
# - /books/<int:pk>/ : GET for detail
# - /books/create/ : POST for create
# - /books/<int:pk>/update/ : PUT/PATCH for update
# - /books/<int:pk>/delete/ : DELETE for delete
# See README for more details and usage instructions.
