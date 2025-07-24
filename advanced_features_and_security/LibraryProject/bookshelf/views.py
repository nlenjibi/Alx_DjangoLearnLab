from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import Book
from .forms import BookForm

# Book List View - Requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books.
    Requires 'can_view' permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Book Detail View - Requires can_view permission
@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Display details of a specific book.
    Requires 'can_view' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Book Create View - Requires can_create permission
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })

# Book Edit View - Requires can_edit permission
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Edit'
    })

# Book Delete View - Requires can_delete permission
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete an existing book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Function-based view to check user permissions
@login_required
def user_permissions(request):
    """
    Display current user's permissions for debugging/admin purposes.
    """
    user_permissions = request.user.get_all_permissions()
    user_groups = request.user.groups.all()
    
    context = {
        'user_permissions': user_permissions,
        'user_groups': user_groups,
        'has_view': request.user.has_perm('bookshelf.can_view'),
        'has_create': request.user.has_perm('bookshelf.can_create'),
        'has_edit': request.user.has_perm('bookshelf.can_edit'),
        'has_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    
    return render(request, 'bookshelf/user_permissions.html', context)
