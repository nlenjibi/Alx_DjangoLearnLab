from django.db import models

# Author model represents a book author.
# Each author can have multiple books (one-to-many relationship).
class Author(models.Model):
	name = models.CharField(max_length=255, help_text="The author's name.")

	def __str__(self):
		return self.name

# Book model represents a book written by an author.
# Each book is linked to one author via a ForeignKey.
class Book(models.Model):
	title = models.CharField(max_length=255, help_text="The book's title.")
	publication_year = models.IntegerField(help_text="Year the book was published.")
	author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, help_text="Reference to the author of the book.")

	def __str__(self):
		return f"{self.title} ({self.publication_year})"

# Create your models here.
