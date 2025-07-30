from django.shortcuts import render
from rest_framework import generics
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


# Create your views here.
