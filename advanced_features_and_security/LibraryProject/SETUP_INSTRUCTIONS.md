# Django Security Implementation - Setup Instructions

## Quick Start

### 1. Run the Setup Script

```bash
python setup_security.py
```

This automated script will:

- Run database migrations
- Set up user groups and permissions
- Create test users
- Run security checks
- Display a complete setup summary

### 2. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install Pillow for ImageField support
pip install Pillow

# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Set up groups and permissions
python manage.py setup_groups

# Create test users
python manage.py create_test_users

# Create a superuser
python manage.py createsuperuser

# Run security checks
python manage.py check --deploy
```

### 3. Start the Server

```bash
python manage.py runserver
```

### 4. Test the Application

Visit these URLs to explore the security features:

- **Main Application:** http://127.0.0.1:8000/bookshelf/
- **Security Demo:** http://127.0.0.1:8000/bookshelf/form-example/
- **User Permissions:** http://127.0.0.1:8000/bookshelf/permissions/
- **Admin Panel:** http://127.0.0.1:8000/admin/

### 5. Test Users

Login with these test accounts to see different permission levels:

- **Viewer:** `viewer_test` / `testpass123` (can only view books)
- **Editor:** `editor_test` / `testpass123` (can view, create, edit books)
- **Admin:** `admin_test` / `testpass123` (full access to all operations)

## Security Features Implemented

### ✅ Custom User Model

- Extended AbstractUser with `date_of_birth` and `profile_photo` fields
- Custom user manager for user creation
- Proper admin integration

### ✅ CSRF Protection

- CSRF tokens in all forms
- Middleware protection enabled
- Secure cookie settings

### ✅ XSS Prevention

- Auto-escaping in templates
- Input validation and sanitization
- Content Security Policy headers

### ✅ SQL Injection Prevention

- Django ORM parameterized queries
- No raw SQL or string formatting
- Secure search implementation

### ✅ Access Control

- Permission-based view protection
- Custom permissions: can_view, can_create, can_edit, can_delete
- User groups: Viewers, Editors, Admins
- Template-level permission checks

### ✅ Security Headers

- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Content Security Policy
- Referrer Policy

### ✅ Input Validation

- Comprehensive form validation
- Length restrictions
- Character pattern validation
- Business logic validation

### ✅ Security Logging

- Failed authentication attempts
- Suspicious request patterns
- Administrative actions
- Form validation errors

### ✅ Secure Settings

- Password validators
- Session security
- Cookie security
- HTTPS settings (for production)

## Testing Security

### Automated Testing

```bash
# Run the security test suite
python test_security.py
```

### Manual Testing

1. **Test CSRF Protection:**

   - Try submitting forms without CSRF tokens
   - Should receive 403 Forbidden errors

2. **Test XSS Prevention:**

   - Enter `<script>alert('XSS')</script>` in form fields
   - Should be escaped and not executed

3. **Test SQL Injection:**

   - Enter `'; DROP TABLE bookshelf_book; --` in search
   - Should be safely handled by ORM

4. **Test Access Control:**

   - Login as different users
   - Verify permission restrictions work
   - Try accessing URLs directly without permissions

5. **Test Input Validation:**
   - Enter overly long text
   - Enter invalid characters
   - Leave required fields empty
   - Should see appropriate error messages
     python manage.py runserver

```

## URL Patterns Available

After running the server, you can access:

- Books List: http://127.0.0.1:8000/books/
- Library Detail: http://127.0.0.1:8000/library/<id>/
- Login: http://127.0.0.1:8000/login/
- Logout: http://127.0.0.1:8000/logout/
- Register: http://127.0.0.1:8000/register/
- Admin: http://127.0.0.1:8000/admin/

## Features Implemented

1. Function-based view for listing books
2. Class-based DetailView for library details
3. User authentication (login, logout, register)
4. Templates with navigation and user authentication status
5. URL routing for all views
6. Models with proper relationships and publication_year field
```
