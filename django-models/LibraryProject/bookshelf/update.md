
---

###  `update.md`
```markdown
# Update the Book's title

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
