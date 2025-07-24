from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Custom admin configuration for CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model with additional fields.
    """
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    
    # Fields to filter by in the admin sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    
    # Fields to search by
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Ordering
    ordering = ('username',)
    
    # Add the custom fields to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Add the custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )

# Custom admin configuration for Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')     # Show these fields in list view
    list_filter = ('publication_year',)                        # Filter sidebar by publication year
    search_fields = ('title', 'author')                        # Search bar for title and author

# Alternative explicit registration (both methods work)
# admin.site.register(CustomUser, CustomUserAdmin)
