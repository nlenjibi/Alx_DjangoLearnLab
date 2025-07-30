from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view handles GET requests to return all books in JSON format.
    Uses the BookSerializer to convert Book model instances to JSON.
    
    Permissions: Requires authentication to view books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for the Book model.
    
    Actions:
    - GET /api/books_all/ - List all books (requires authentication)
    - POST /api/books_all/ - Create a new book (requires authentication)
    - GET /api/books_all/{id}/ - Retrieve a specific book (requires authentication)
    - PUT /api/books_all/{id}/ - Update a specific book (requires authentication)
    - PATCH /api/books_all/{id}/ - Partially update a specific book (requires authentication)
    - DELETE /api/books_all/{id}/ - Delete a specific book (requires authentication)
    
    Permissions:
    - List and Retrieve: Any authenticated user
    - Create, Update, Delete: Authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Anyone authenticated can view books
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only authenticated users can create, update, or delete
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """
        Create a new book instance.
        Only authenticated users can create books.
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
        Only authenticated users can update books.
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
        Only authenticated users can delete books.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom token authentication view that returns additional user information.
    
    POST /api/auth/token/
    Body: {"username": "your_username", "password": "your_password"}
    Returns: {"token": "your_token", "user_id": 1, "username": "your_username"}
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })


# Create your views here.
