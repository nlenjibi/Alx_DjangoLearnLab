from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from django.db.models import Q
import logging
import re

from .models import Book
from .forms import BookForm

# Set up security logging
logger = logging.getLogger('django.security')

# Book List View with Security Enhancements
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_list(request):
    """
    Display a list of all books with optional search functionality.
    Implements secure search to prevent SQL injection.
    Requires 'can_view' permission.
    """
    books = Book.objects.all()
    search_query = None
    
    # Secure search implementation
    if request.method == "POST" or request.GET.get('search'):
        search_query = request.POST.get('search') or request.GET.get('search')
        
        if search_query:
            # Sanitize and validate search input
            search_query = escape(search_query.strip())
            
            # Log search attempts for security monitoring
            logger.info(f"Search performed by user {request.user.username}: '{search_query}'")
            
            # Validate search query length to prevent DoS
            if len(search_query) > 100:
                messages.error(request, "Search query too long. Please limit to 100 characters.")
                return redirect('bookshelf:book_list')
            
            # Use Django ORM's secure parameterized queries
            books = books.filter(
                Q(title__icontains=search_query) | 
                Q(author__icontains=search_query)
            )
    
    context = {
        'books': books,
        'search_query': search_query,
    }
    return render(request, 'bookshelf/book_list.html', context)

# Book Detail View with Security Enhancements
@permission_required('bookshelf.can_view', raise_exception=True)
@csrf_protect
@require_http_methods(["GET"])
def book_detail(request, pk):
    """
    Display details of a specific book with input validation.
    Requires 'can_view' permission.
    """
    try:
        # Validate that pk is a positive integer
        pk = int(pk)
        if pk <= 0:
            raise ValueError("Invalid book ID")
    except (ValueError, TypeError):
        logger.warning(f"Invalid book ID attempted by user {request.user.username}: {pk}")
        messages.error(request, "Invalid book ID.")
        return redirect('bookshelf:book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    # Log book access for audit trail
    logger.info(f"Book '{book.title}' accessed by user {request.user.username}")
    
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Book Create View with Enhanced Security
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_create(request):
    """
    Create a new book with comprehensive input validation.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        
        # Additional server-side validation
        if form.is_valid():
            try:
                book = form.save()
                
                # Log successful creation
                logger.info(f"Book '{book.title}' created by user {request.user.username}")
                
                messages.success(request, f'Book "{escape(book.title)}" created successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
                
            except ValidationError as e:
                logger.warning(f"Validation error during book creation by {request.user.username}: {e}")
                messages.error(request, "Invalid data provided. Please check your input.")
            except Exception as e:
                logger.error(f"Unexpected error during book creation by {request.user.username}: {e}")
                messages.error(request, "An error occurred while creating the book.")
        else:
            # Log form validation errors
            logger.warning(f"Form validation failed for user {request.user.username}: {form.errors}")
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'action': 'Create'
    })

# Book Edit View with Enhanced Security
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    """
    Edit an existing book with comprehensive security measures.
    Requires 'can_edit' permission.
    """
    try:
        # Validate that pk is a positive integer
        pk = int(pk)
        if pk <= 0:
            raise ValueError("Invalid book ID")
    except (ValueError, TypeError):
        logger.warning(f"Invalid book ID attempted for edit by user {request.user.username}: {pk}")
        messages.error(request, "Invalid book ID.")
        return redirect('bookshelf:book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            try:
                original_title = book.title
                book = form.save()
                
                # Log successful update
                logger.info(f"Book '{original_title}' updated to '{book.title}' by user {request.user.username}")
                
                messages.success(request, f'Book "{escape(book.title)}" updated successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
                
            except ValidationError as e:
                logger.warning(f"Validation error during book update by {request.user.username}: {e}")
                messages.error(request, "Invalid data provided. Please check your input.")
            except Exception as e:
                logger.error(f"Unexpected error during book update by {request.user.username}: {e}")
                messages.error(request, "An error occurred while updating the book.")
        else:
            # Log form validation errors
            logger.warning(f"Form validation failed for book edit by user {request.user.username}: {form.errors}")
    else:
        form = BookForm(instance=book)
        
        # Log book edit access
        logger.info(f"Book '{book.title}' edit form accessed by user {request.user.username}")
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Edit'
    })

# Book Delete View with Enhanced Security
@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    """
    Delete an existing book with security logging and validation.
    Requires 'can_delete' permission.
    """
    try:
        # Validate that pk is a positive integer
        pk = int(pk)
        if pk <= 0:
            raise ValueError("Invalid book ID")
    except (ValueError, TypeError):
        logger.warning(f"Invalid book ID attempted for deletion by user {request.user.username}: {pk}")
        messages.error(request, "Invalid book ID.")
        return redirect('bookshelf:book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            title = book.title
            book_id = book.pk
            book.delete()
            
            # Log successful deletion
            logger.warning(f"Book '{title}' (ID: {book_id}) deleted by user {request.user.username}")
            
            messages.success(request, f'Book "{escape(title)}" deleted successfully!')
            return redirect('bookshelf:book_list')
            
        except Exception as e:
            logger.error(f"Error deleting book by user {request.user.username}: {e}")
            messages.error(request, "An error occurred while deleting the book.")
            return redirect('bookshelf:book_detail', pk=book.pk)
    else:
        # Log delete confirmation page access
        logger.info(f"Book '{book.title}' delete confirmation accessed by user {request.user.username}")
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Enhanced User Permissions View
@login_required
@csrf_protect
@require_http_methods(["GET"])
def user_permissions(request):
    """
    Display current user's permissions with security context.
    """
    try:
        user_permissions = request.user.get_all_permissions()
        user_groups = request.user.groups.all()
        
        # Log permissions access for audit trail
        logger.info(f"User permissions viewed by {request.user.username}")
        
        context = {
            'user_permissions': user_permissions,
            'user_groups': user_groups,
            'has_view': request.user.has_perm('bookshelf.can_view'),
            'has_create': request.user.has_perm('bookshelf.can_create'),
            'has_edit': request.user.has_perm('bookshelf.can_edit'),
            'has_delete': request.user.has_perm('bookshelf.can_delete'),
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        }
        
        return render(request, 'bookshelf/user_permissions.html', context)
        
    except Exception as e:
        logger.error(f"Error accessing user permissions for {request.user.username}: {e}")
        messages.error(request, "Unable to load permissions information.")
        return redirect('bookshelf:book_list')

# Secure Form Example View
@login_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def form_example(request):
    """
    Display a comprehensive form example showing security best practices.
    """
    if request.method == 'POST':
        # Process the form with full security validation
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        publication_year = request.POST.get('publication_year')
        
        # Log form submission attempt
        logger.info(f"Secure form submission by user {request.user.username}")
        
        # Comprehensive validation
        errors = []
        
        # Title validation
        if not title:
            errors.append("Title is required.")
        elif len(title) < 2 or len(title) > 200:
            errors.append("Title must be between 2 and 200 characters.")
        elif not re.match(r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\(\)\'\"]+$', title):
            errors.append("Title contains invalid characters.")
        
        # Author validation
        if not author:
            errors.append("Author is required.")
        elif len(author) < 2 or len(author) > 100:
            errors.append("Author must be between 2 and 100 characters.")
        elif not re.match(r'^[a-zA-Z\s\-\.\']+$', author):
            errors.append("Author name contains invalid characters.")
        
        # Year validation
        try:
            year = int(publication_year) if publication_year else None
            if not year:
                errors.append("Publication year is required.")
            elif year < 1000 or year > 2030:
                errors.append("Publication year must be between 1000 and 2030.")
        except (ValueError, TypeError):
            errors.append("Publication year must be a valid number.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # All validation passed
            messages.success(request, f"✅ Form validation successful! Book '{escape(title)}' by {escape(author)} ({year}) would be created.")
            logger.info(f"Secure form validation passed for user {request.user.username}: {title} by {author}")
    
    return render(request, 'bookshelf/form_example.html')
