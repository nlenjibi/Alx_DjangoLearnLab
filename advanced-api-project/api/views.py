from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# BookListView: Retrieves all books.
# Allows read-only access to unauthenticated users.
class BookListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	# Enable filtering, searching, and ordering
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	filterset_fields = ['title', 'author', 'publication_year']  # Filter by these fields
	search_fields = ['title', 'author__name']  # Search by book title or author name
	ordering_fields = ['title', 'publication_year', 'author']  # Order by these fields
	ordering = ['title']  # Default ordering

	# Documentation:
	# Filtering: /api/books/?title=BookTitle&author=1&publication_year=2020
	# Searching: /api/books/?search=SomeText
	# Ordering: /api/books/?ordering=title or /api/books/?ordering=-publication_year
	# See README for more examples.

# BookDetailView: Retrieves a single book by ID.
# Allows read-only access to unauthenticated users.
class BookDetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

# BookCreateView: Adds a new book.
# Only authenticated users can create books.
class BookCreateView(generics.CreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	# Customization: You can override perform_create to add custom logic.
	def perform_create(self, serializer):
		# Example: Add custom logic here if needed
		serializer.save()

# BookUpdateView: Modifies an existing book.
# Only authenticated users can update books.
class BookUpdateView(generics.UpdateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	# Customization: You can override perform_update to add custom logic.
	def perform_update(self, serializer):
		# Example: Add custom logic here if needed
		serializer.save()

# BookDeleteView: Removes a book.
# Only authenticated users can delete books.
class BookDeleteView(generics.DestroyAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]

	# Customization: You can override perform_destroy to add custom logic.
	def perform_destroy(self, instance):
		# Example: Add custom logic here if needed
		instance.delete()

# Documentation:
# - Each view uses DRF generic views for CRUD operations.
# - Permission classes restrict write operations to authenticated users.
# - Custom hooks (perform_create, perform_update, perform_destroy) allow further customization.
# - See README for endpoint details and usage instructions.
