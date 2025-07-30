from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Create test users and tokens for API authentication testing'
    
    def handle(self, *args, **options):
        # Create test users
        users_data = [
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'User'
            },
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'adminpass123',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        ]
        
        for user_data in users_data:
            username = user_data['username']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists. Skipping...')
                )
                continue
            
            # Create user
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            
            # Create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Token for {username}: {token.key}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Test users created successfully!')
        )
        self.stdout.write(
            self.style.WARNING('Please save these tokens for testing!')
        )
