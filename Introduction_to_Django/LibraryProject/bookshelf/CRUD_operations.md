# CRUD Operations for Book Model Using Django ORM

This file documents the Create, Retrieve, Update, and Delete (CRUD) operations performed using the Django shell on the `Book` model from the `bookshelf` app in the `LibraryProject`.

---

## 1 CREATE: Add a Book to the Database

### Commands:
```python
from bookshelf.models import Book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()

### output
>>> book
<Book: Book object (1)>

RetrieveCommand:

Copy code
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

Output:

Copy code
1984 George Orwell 1949

Update
Command:
python
Copy code
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
Output:
python
Copy code
>>> book.title
'Nineteen Eighty-Four'
 Title updated from "1984" to "Nineteen Eighty-Four".

 Delete
Command:
python
Copy code
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Output:


(1, {'bookshelf.Book': 1})

Confirm Deletion:
Book.objects.all()

Output:

<QuerySet []>