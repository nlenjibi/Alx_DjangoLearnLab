from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# BookListView: Retrieves all books.
# Allows read-only access to unauthenticated users.
class BookListView(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

# BookDetailView: Retrieves a single book by ID.
# Allows read-only access to unauthenticated users.
class BookDetailView(generics.RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

# BookCreateView: Adds a new book.
# Only authenticated users can create books.
class BookCreateView(generics.CreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	# Customization: You can override perform_create to add custom logic.
	def perform_create(self, serializer):
		# Example: Add custom logic here if needed
		serializer.save()

# BookUpdateView: Modifies an existing book.
# Only authenticated users can update books.
class BookUpdateView(generics.UpdateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	# Customization: You can override perform_update to add custom logic.
	def perform_update(self, serializer):
		# Example: Add custom logic here if needed
		serializer.save()

# BookDeleteView: Removes a book.
# Only authenticated users can delete books.
class BookDeleteView(generics.DestroyAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	# Customization: You can override perform_destroy to add custom logic.
	def perform_destroy(self, instance):
		# Example: Add custom logic here if needed
		instance.delete()

# Documentation:
# - Each view uses DRF generic views for CRUD operations.
# - Permission classes restrict write operations to authenticated users.
# - Custom hooks (perform_create, perform_update, perform_destroy) allow further customization.
# - See README for endpoint details and usage instructions.
