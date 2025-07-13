# Creating a Book Instance

To create and save a new `Book` object in Django, use the following code:

```python
from bookshelf.models import Book

book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```
