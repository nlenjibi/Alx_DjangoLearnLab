# Django Permissions and Groups Setup Guide

## Overview

This Django application implements a comprehensive permissions and groups system to control access to the Bookshelf app functionality. The system uses Django's built-in permissions framework with custom permissions to provide fine-grained access control.

## Custom Permissions

### Bookshelf App Permissions

The following custom permissions are defined in the `Book` model (`bookshelf/models.py`):

1. **`can_view`** - Allows users to view books and book details
2. **`can_create`** - Allows users to create new books
3. **`can_edit`** - Allows users to edit existing books
4. **`can_delete`** - Allows users to delete books

### Permission Implementation

```python
class Book(models.Model):
    # ... model fields ...

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
```

## Recommended Groups Setup

### 1. Viewers Group

**Permissions:**

- `bookshelf.can_view`

**Purpose:** Users who can only browse and view books but cannot make any changes.

### 2. Editors Group

**Permissions:**

- `bookshelf.can_view`
- `bookshelf.can_create`
- `bookshelf.can_edit`

**Purpose:** Users who can view, create, and edit books but cannot delete them.

### 3. Admins Group

**Permissions:**

- `bookshelf.can_view`
- `bookshelf.can_create`
- `bookshelf.can_edit`
- `bookshelf.can_delete`

**Purpose:** Users with full access to all book operations.

## Setting Up Groups and Permissions

### Step 1: Create Groups in Django Admin

1. Navigate to Django Admin (`/admin/`)
2. Go to **Authentication and Authorization > Groups**
3. Click **Add Group**
4. Create the following groups:
   - `Viewers`
   - `Editors`
   - `Admins`

### Step 2: Assign Permissions to Groups

For each group created above:

1. **Viewers Group:**

   - Select: `bookshelf | book | Can view book`

2. **Editors Group:**

   - Select: `bookshelf | book | Can view book`
   - Select: `bookshelf | book | Can create book`
   - Select: `bookshelf | book | Can edit book`

3. **Admins Group:**
   - Select: `bookshelf | book | Can view book`
   - Select: `bookshelf | book | Can create book`
   - Select: `bookshelf | book | Can edit book`
   - Select: `bookshelf | book | Can delete book`

### Step 3: Assign Users to Groups

1. Go to **Authentication and Authorization > Users**
2. Select a user to edit
3. In the **Permissions** section, under **Groups**, select the appropriate group(s)
4. Save the user

## View-Level Permission Enforcement

### Permission Decorators Used

All views in `bookshelf/views.py` use Django's `@permission_required` decorator:

```python
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    # View implementation

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    # View implementation

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    # View implementation
```

### Permission Checking in Templates

Templates use Django's built-in permission checking:

```html
{% if user.has_perm:'bookshelf.can_create' %}
<a href="{% url 'bookshelf:book_create' %}" class="btn btn-success">Add Book</a>
{% endif %} {% if user.has_perm:'bookshelf.can_edit' %}
<a href="{% url 'bookshelf:book_edit' book.pk %}" class="btn btn-primary"
  >Edit</a
>
{% endif %}
```

## Testing the Permission System

### 1. Create Test Users

Create users with different permission levels:

```bash
# In Django shell (python manage.py shell)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Create test users
viewer_user = User.objects.create_user('viewer_test', 'viewer@example.com', 'password123')
editor_user = User.objects.create_user('editor_test', 'editor@example.com', 'password123')
admin_user = User.objects.create_user('admin_test', 'admin@example.com', 'password123')

# Assign to groups
viewers_group = Group.objects.get(name='Viewers')
editors_group = Group.objects.get(name='Editors')
admins_group = Group.objects.get(name='Admins')

viewer_user.groups.add(viewers_group)
editor_user.groups.add(editors_group)
admin_user.groups.add(admins_group)
```

### 2. Manual Testing Procedure

1. **Test Viewer User:**

   - Login as viewer_test
   - Should be able to view book list and details
   - Should NOT see "Add Book", "Edit", or "Delete" buttons
   - Attempting to access create/edit/delete URLs directly should result in 403 Forbidden

2. **Test Editor User:**

   - Login as editor_test
   - Should be able to view, create, and edit books
   - Should NOT see "Delete" buttons
   - Attempting to access delete URLs directly should result in 403 Forbidden

3. **Test Admin User:**
   - Login as admin_test
   - Should have full access to all operations
   - Should see all buttons and be able to perform all actions

### 3. Automated Testing

Consider adding unit tests to verify permission enforcement:

```python
# In bookshelf/tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.urls import reverse

class PermissionTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.client = Client()

        # Create test user without permissions
        self.user_no_perms = User.objects.create_user('noperms', 'no@example.com', 'pass')

        # Test accessing protected views
        self.client.login(username='noperms', password='pass')
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 403)  # Should be forbidden
```

## Security Considerations

1. **Always use `raise_exception=True`** in permission decorators to return 403 Forbidden instead of redirecting to login
2. **Check permissions in templates** to hide UI elements users cannot access
3. **Never rely solely on UI hiding** - always enforce permissions at the view level
4. **Use Django's built-in permission system** rather than custom implementations
5. **Regular audit** of user groups and permissions

## URLs and Navigation

The bookshelf app provides the following protected URLs:

- `/bookshelf/` - Book list (requires `can_view`)
- `/bookshelf/book/<id>/` - Book detail (requires `can_view`)
- `/bookshelf/book/create/` - Create book (requires `can_create`)
- `/bookshelf/book/<id>/edit/` - Edit book (requires `can_edit`)
- `/bookshelf/book/<id>/delete/` - Delete book (requires `can_delete`)
- `/bookshelf/permissions/` - View user permissions (login required)

## Troubleshooting

### Common Issues:

1. **Permission not found errors:**

   - Ensure you've run migrations after defining custom permissions
   - Check that the permission codename matches exactly

2. **Users can't access anything:**

   - Verify the user is assigned to the correct group
   - Check that the group has the required permissions

3. **Permissions not working in templates:**

   - Ensure you're using the correct permission format: `app_label.permission_codename`
   - Example: `bookshelf.can_view`, not just `can_view`

4. **403 Forbidden errors:**
   - This is expected behavior when users lack required permissions
   - Customize the 403 error template if needed

## Additional Resources

- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django Groups Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)
- [Permission Decorators](https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator)
