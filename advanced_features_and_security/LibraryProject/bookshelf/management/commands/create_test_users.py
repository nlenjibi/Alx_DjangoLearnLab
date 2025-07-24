from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for different permission levels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing test users before creating new ones',
        )

    def handle(self, *args, **options):
        if options['reset']:
            # Delete existing test users
            test_usernames = ['viewer_test', 'editor_test', 'admin_test']
            deleted_count = User.objects.filter(username__in=test_usernames).count()
            User.objects.filter(username__in=test_usernames).delete()
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing test users')
            )
        
        # Get groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found! Run: python manage.py setup_groups')
            )
            return
        
        # Create test users
        test_users = [
            {
                'username': 'viewer_test',
                'email': 'viewer@example.com',
                'password': 'testpass123',
                'group': viewers_group,
                'description': 'Can only view books'
            },
            {
                'username': 'editor_test',
                'email': 'editor@example.com',
                'password': 'testpass123',
                'group': editors_group,
                'description': 'Can view, create, and edit books'
            },
            {
                'username': 'admin_test',
                'email': 'admin@example.com',
                'password': 'testpass123',
                'group': admins_group,
                'description': 'Full access to all book operations'
            }
        ]
        
        created_users = []
        
        for user_data in test_users:
            username = user_data['username']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists, skipping...')
                )
                continue
            
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            # Add to group
            user.groups.add(user_data['group'])
            
            created_users.append(user_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'Created user "{username}" in group "{user_data["group"].name}"')
            )
        
        if created_users:
            self.stdout.write('\n' + '='*60)
            self.stdout.write('TEST USERS CREATED:')
            self.stdout.write('='*60)
            
            for user_data in created_users:
                self.stdout.write(f'\nUsername: {user_data["username"]}')
                self.stdout.write(f'Password: {user_data["password"]}')
                self.stdout.write(f'Group: {user_data["group"].name}')
                self.stdout.write(f'Permissions: {user_data["description"]}')
            
            self.stdout.write('\n' + '='*60)
            self.stdout.write('TESTING INSTRUCTIONS:')
            self.stdout.write('1. Visit /bookshelf/ to test the permission system')
            self.stdout.write('2. Login with each test user to verify their access levels')
            self.stdout.write('3. Check /bookshelf/permissions/ to see user permissions')
            self.stdout.write('='*60)
        else:
            self.stdout.write(
                self.style.WARNING('No new users were created (all already exist)')
            )
