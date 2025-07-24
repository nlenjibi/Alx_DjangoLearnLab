# Setup instructions for the Django project

## Migration Commands

To apply the model changes (including the new publication_year field), run the following commands:

```bash
# Navigate to the project directory
cd c:\Users\ModernTech\Desktop\react\django\Alx_DjangoLearnLab\django-models\LibraryProject

# Create migrations for the new publication_year field
python manage.py makemigrations relationship_app

# Apply the migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Run the development server
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
