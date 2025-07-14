# Role-Based Access Control Implementation

## Migration Instructions

After implementing the role-based access control system, run the following commands:

```bash
# Navigate to the project directory
cd c:\Users\ModernTech\Desktop\react\django\Alx_DjangoLearnLab\django-models\LibraryProject

# Create migrations for the new UserProfile model
python manage.py makemigrations relationship_app

# Apply the migrations
python manage.py migrate

# Create a superuser for testing
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

## Testing Role-Based Access Control

### Creating Users with Different Roles

1. **Create users through Django Admin:**

   - Go to http://127.0.0.1:8000/admin/
   - Login with your superuser account
   - Create new users and assign roles via UserProfile

2. **Test Access Control:**
   - Login as different users
   - Try accessing role-specific URLs:
     - `/admin/` - Only Admin users
     - `/librarian/` - Only Librarian users
     - `/member/` - Only Member users

### URL Patterns Available

- **Public Access:**

  - `/books/` - List all books
  - `/login/` - User login
  - `/register/` - User registration
  - `/logout/` - User logout

- **Role-Based Access:**
  - `/admin/` - Admin dashboard (Admin role only)
  - `/librarian/` - Librarian dashboard (Librarian role only)
  - `/member/` - Member dashboard (Member role only)

### Features Implemented

1. **UserProfile Model:**

   - One-to-one relationship with Django User
   - Role field with choices: Admin, Librarian, Member
   - Automatic profile creation using Django signals

2. **Access Control:**

   - `@user_passes_test` decorators for role checking
   - Helper functions to verify user roles
   - Secure access to role-specific views

3. **Role-Based Templates:**

   - Distinct dashboards for each role
   - Role-specific navigation and content
   - Professional styling and layout

4. **User Experience:**
   - Dynamic navigation based on user role
   - Clear role identification in templates
   - Seamless integration with existing authentication

## Notes

- New users will automatically get a UserProfile with 'Member' as default role
- Admins can change user roles through the Django admin interface
- Each role has specific permissions and access levels
- The system is extensible for adding more roles in the future
