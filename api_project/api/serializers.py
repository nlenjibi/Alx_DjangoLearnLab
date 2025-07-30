from rest_framework import serializers
from .models import Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to JSON format and vice versa.
    Includes validation for CRUD operations.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model
        
    def validate_isbn(self, value):
        """
        Custom validation for ISBN field.
        Ensures ISBN is exactly 13 characters and unique.
        """
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters long.")
        
        # Check for uniqueness during updates
        if self.instance and self.instance.isbn != value:
            if Book.objects.filter(isbn=value).exists():
                raise serializers.ValidationError("A book with this ISBN already exists.")
        elif not self.instance and Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("A book with this ISBN already exists.")
        
        return value
    
    def validate_published_date(self, value):
        """
        Custom validation for published_date field.
        Ensures the date is not in the future.
        """
        if value and value > date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value
    
    def validate_title(self, value):
        """
        Custom validation for title field.
        Ensures title is not empty after stripping whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_author(self, value):
        """
        Custom validation for author field.
        Ensures author is not empty after stripping whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Author cannot be empty.")
        return value.strip()
