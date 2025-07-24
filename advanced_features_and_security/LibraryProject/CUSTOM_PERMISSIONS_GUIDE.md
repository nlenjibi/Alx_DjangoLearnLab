# Custom Permissions Implementation Guide

## Overview

This implementation adds custom permissions to the Django Book model to control access to specific actions (add, edit, delete) based on user permissions.

## Migration Instructions

```bash
# Navigate to project directory
cd c:\Users\ModernTech\Desktop\react\django\Alx_DjangoLearnLab\django-models\LibraryProject

# Create migrations for the custom permissions
python manage.py makemigrations relationship_app

# Apply migrations
python manage.py migrate

# Create superuser for testing permissions
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Custom Permissions Added

### Book Model Permissions

- `can_add_book` - Permission to add new books
- `can_change_book` - Permission to edit existing books
- `can_delete_book` - Permission to delete books

## Views with Permission Control

### Permission-Secured Views

1. **add_book** - Requires `relationship_app.can_add_book` permission
2. **edit_book** - Requires `relationship_app.can_change_book` permission
3. **delete_book** - Requires `relationship_app.can_delete_book` permission

### Access Control Features

- Uses `@permission_required` decorator with `raise_exception=True`
- Automatically raises 403 Forbidden for unauthorized users
- Integrates with Django's permission system

## URL Patterns

### New Permission-Secured URLs

- `/add_book/` - Add new book (requires add permission)
- `/edit_book/<int:book_id>/` - Edit book (requires change permission)
- `/delete_book/<int:book_id>/` - Delete book (requires delete permission)

## Templates Created

### Book Operation Templates

1. **add_book.html** - Form for adding new books
2. **edit_book.html** - Form for editing existing books
3. **delete_book.html** - Confirmation page for book deletion

### Template Features

- Professional styling and layout
- Form validation and error handling
- Navigation and user-friendly interface
- Permission-based action buttons in book list

## Permission Assignment

### Through Django Admin

1. Login to admin: `/admin/`
2. Go to Users section
3. Select a user to edit
4. In "User permissions" section, add:
   - `relationship_app | book | Can add book`
   - `relationship_app | book | Can change book`
   - `relationship_app | book | Can delete book`

### Through Groups (Recommended)

1. Create groups with specific permissions:
   - **Librarians**: can_add_book, can_change_book
   - **Admins**: can_add_book, can_change_book, can_delete_book
   - **Members**: No book modification permissions

## Testing the Implementation

### Test Cases

1. **Unauthorized Access**: Try accessing secured URLs without permissions
2. **Add Book**: Test with can_add_book permission
3. **Edit Book**: Test with can_change_book permission
4. **Delete Book**: Test with can_delete_book permission
5. **Template Integration**: Verify action buttons appear based on permissions

### Expected Behavior

- Users without permissions see 403 Forbidden error
- Action buttons only appear for users with appropriate permissions
- Forms work correctly with proper validation
- Redirects work as expected after operations

## Security Features

### Access Control

- Permission checks before any book operations
- Template-level permission checks using `{% if perms.app.permission %}`
- Proper error handling for unauthorized access
- CSRF protection on all forms

### Best Practices Implemented

- Separation of concerns (model, view, template)
- RESTful URL patterns
- Proper form handling and validation
- User-friendly error messages and navigation

## Integration with Role-Based Access Control

The custom permissions work alongside the existing role-based system:

- **Roles** define user categories (Admin, Librarian, Member)
- **Permissions** define specific actions users can perform
- Both systems can be used together for fine-grained access control

## File Structure

```
relationship_app/
├── models.py           # Book model with custom permissions
├── views.py            # Permission-secured views
├── urls.py             # URL patterns for secured views
└── templates/relationship_app/
    ├── add_book.html   # Add book form
    ├── edit_book.html  # Edit book form
    ├── delete_book.html # Delete confirmation
    └── list_books.html  # Updated with permission-based actions
```

## Notes

- Custom permissions are automatically created when migrations are applied
- Permissions can be assigned individually or through groups
- The system is extensible for adding more granular permissions
- Integration with existing authentication and role-based systems
