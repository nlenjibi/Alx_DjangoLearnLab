from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view handles GET requests to return all books in JSON format.
    Uses the BookSerializer to convert Book model instances to JSON.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for the Book model.
    
    Actions:
    - GET /books_all/ - List all books
    - POST /books_all/ - Create a new book
    - GET /books_all/{id}/ - Retrieve a specific book
    - PUT /books_all/{id}/ - Update a specific book
    - PATCH /books_all/{id}/ - Partially update a specific book
    - DELETE /books_all/{id}/ - Delete a specific book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new book instance.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a book instance.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a book instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
