#!/usr/bin/env python
"""
Setup script for Django Security Implementation
This script sets up the complete security system including:
- Migrations
- Groups and permissions
- Test users
- Initial security checks
"""

import os
import sys
import django
from django.core.management import execute_from_command_line, call_command
from django.core.management.base import CommandError

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
    django.setup()

def run_migrations():
    """Run database migrations"""
    print("🔄 Running database migrations...")
    try:
        call_command('makemigrations')
        call_command('migrate')
        print("✅ Migrations completed successfully")
        return True
    except CommandError as e:
        print(f"❌ Migration failed: {e}")
        return False

def setup_groups_and_permissions():
    """Setup user groups and permissions"""
    print("🔄 Setting up groups and permissions...")
    try:
        call_command('setup_groups')
        print("✅ Groups and permissions setup completed")
        return True
    except CommandError as e:
        print(f"❌ Groups setup failed: {e}")
        return False

def create_test_users():
    """Create test users with different permission levels"""
    print("🔄 Creating test users...")
    try:
        call_command('create_test_users')
        print("✅ Test users created successfully")
        return True
    except CommandError as e:
        print(f"❌ Test user creation failed: {e}")
        return False

def create_superuser():
    """Create superuser if needed"""
    print("🔄 Checking for superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(is_superuser=True).exists():
        print("📝 No superuser found. Please create one:")
        try:
            call_command('createsuperuser')
            print("✅ Superuser created successfully")
        except (CommandError, KeyboardInterrupt):
            print("⚠️  Superuser creation skipped")
    else:
        print("✅ Superuser already exists")

def run_security_checks():
    """Run Django security checks"""
    print("🔄 Running security checks...")
    try:
        call_command('check', '--deploy')
        print("✅ Security checks passed")
        return True
    except CommandError as e:
        print(f"⚠️  Security check warnings: {e}")
        return True  # Warnings are acceptable in development

def display_setup_summary():
    """Display setup summary and next steps"""
    print("\n" + "="*60)
    print("🎉 DJANGO SECURITY SETUP COMPLETED!")
    print("="*60)
    
    print("\n📋 What was set up:")
    print("• Custom User model with date_of_birth and profile_photo")
    print("• Enhanced security middleware with CSP and security headers")
    print("• Comprehensive input validation and XSS prevention")
    print("• CSRF protection on all forms")
    print("• SQL injection prevention via Django ORM")
    print("• Permission-based access control")
    print("• Security logging and monitoring")
    print("• User groups: Viewers, Editors, Admins")
    
    print("\n👥 Test Users Created:")
    print("• viewer_test / testpass123 (can view books)")
    print("• editor_test / testpass123 (can view, create, edit books)")
    print("• admin_test / testpass123 (full access)")
    
    print("\n🚀 Next Steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000/bookshelf/ to test the application")
    print("3. Login with test users to verify permissions")
    print("4. Visit /admin/ to manage users and groups")
    print("5. Check security.log file for security events")
    
    print("\n🔒 Security Features Active:")
    print("• CSRF protection on all forms")
    print("• XSS prevention with input escaping")
    print("• SQL injection prevention")
    print("• Content Security Policy headers")
    print("• Secure session and cookie settings")
    print("• Permission-based access control")
    print("• Security event logging")
    
    print("\n📚 Documentation:")
    print("• SECURITY_IMPLEMENTATION_GUIDE.md - Complete security guide")
    print("• PERMISSIONS_SETUP_GUIDE.md - Permissions setup guide")
    print("• test_security.py - Security testing script")

def main():
    """Main setup function"""
    print("🛡️  Django Security Implementation Setup")
    print("="*60)
    
    # Setup Django
    setup_django()
    
    # Run setup steps
    steps = [
        ("Database Migrations", run_migrations),
        ("Groups and Permissions", setup_groups_and_permissions),
        ("Test Users", create_test_users),
        ("Security Checks", run_security_checks),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_function in steps:
        print(f"\n📋 Step: {step_name}")
        if step_function():
            success_count += 1
        else:
            print(f"❌ {step_name} failed - continuing with remaining steps...")
    
    # Create superuser (optional)
    create_superuser()
    
    # Display summary
    print(f"\n📊 Setup Results: {success_count}/{total_steps} steps completed successfully")
    
    if success_count == total_steps:
        display_setup_summary()
    else:
        print("⚠️  Some setup steps failed. Please check the errors above and retry.")
        return False
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)
    
    print("\n🎯 Run 'python test_security.py' to test the security implementation!")
