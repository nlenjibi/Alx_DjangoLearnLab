# Creating a Book Instance

To create and save a new `Book` object in Django, you can use either the `save()` method or the `objects.create()` method.

**Using `save()`:**

```python
from bookshelf.models import Book

book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

**Using `objects.create()`:**

```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
```

Both approaches will add a new `Book` record to your database.
