from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Set up groups and permissions for the bookshelf app'

    def handle(self, *args, **options):
        # Get the Book content type
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create the custom permissions
        can_view, created = Permission.objects.get_or_create(
            codename='can_view',
            name='Can view book',
            content_type=book_content_type,
        )
        
        can_create, created = Permission.objects.get_or_create(
            codename='can_create',
            name='Can create book',
            content_type=book_content_type,
        )
        
        can_edit, created = Permission.objects.get_or_create(
            codename='can_edit',
            name='Can edit book',
            content_type=book_content_type,
        )
        
        can_delete, created = Permission.objects.get_or_create(
            codename='can_delete',
            name='Can delete book',
            content_type=book_content_type,
        )
        
        # Create groups and assign permissions
        
        # Viewers Group - can only view books
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        viewers_group.permissions.set([can_view])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created "Viewers" group with view permissions')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Updated "Viewers" group permissions')
            )
        
        # Editors Group - can view, create, and edit books
        editors_group, created = Group.objects.get_or_create(name='Editors')
        editors_group.permissions.set([can_view, can_create, can_edit])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created "Editors" group with view, create, edit permissions')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Updated "Editors" group permissions')
            )
        
        # Admins Group - full permissions
        admins_group, created = Group.objects.get_or_create(name='Admins')
        admins_group.permissions.set([can_view, can_create, can_edit, can_delete])
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created "Admins" group with all permissions')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Updated "Admins" group permissions')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\nGroups and permissions setup completed!')
        )
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SUMMARY:')
        self.stdout.write('='*50)
        
        for group in [viewers_group, editors_group, admins_group]:
            self.stdout.write(f'\n{group.name} Group:')
            for perm in group.permissions.all():
                self.stdout.write(f'  - {perm.name}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('Next Steps:')
        self.stdout.write('1. Go to Django Admin (/admin/)')
        self.stdout.write('2. Create or edit users')
        self.stdout.write('3. Assign users to appropriate groups')
        self.stdout.write('4. Test the permissions system')
        self.stdout.write('='*50)
