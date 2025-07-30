from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to JSON format and vice versa.
    """
    
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model
        
    def validate_isbn(self, value):
        """
        Custom validation for ISBN field.
        Ensures ISBN is exactly 13 characters.
        """
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters long.")
        return value
