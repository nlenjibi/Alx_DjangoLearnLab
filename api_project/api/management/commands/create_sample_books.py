from django.core.management.base import BaseCommand
from api.models import Book
from datetime import date


class Command(BaseCommand):
    help = 'Create sample books for testing the API'
    
    def handle(self, *args, **options):
        # Clear existing books
        Book.objects.all().delete()
        
        # Create sample books
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'published_date': date(1925, 4, 10),
                'isbn': '9780743273565'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'published_date': date(1960, 7, 11),
                'isbn': '9780061120084'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'published_date': date(1949, 6, 8),
                'isbn': '9780451524935'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'published_date': date(1813, 1, 28),
                'isbn': '9780141439518'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'published_date': date(1951, 7, 16),
                'isbn': '9780316769174'
            }
        ]
        
        for book_data in books_data:
            book = Book.objects.create(**book_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created book: {book.title}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(books_data)} books!')
        )
