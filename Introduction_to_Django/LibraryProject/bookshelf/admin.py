from django.contrib import admin
from .models import Book

# Custom admin configuration for Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')     # Show these fields in list view
    list_filter = ('publication_year',)                        # Filter sidebar by publication year
    search_fields = ('title', 'author')                        # Search bar for title and author
