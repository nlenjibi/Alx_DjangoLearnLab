from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
from .models import Book

class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing Book instances with comprehensive validation.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200,
                'required': True,
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100,
                'required': True,
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year',
                'min': 1000,
                'max': 2030,
                'required': True,
            }),
        }
    
    def clean_title(self):
        """
        Validate and sanitize book title.
        """
        title = self.cleaned_data.get('title', '').strip()
        
        if not title:
            raise ValidationError("Title is required.")
        
        # Check for minimum length
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        
        # Check for suspicious characters that might indicate injection attempts
        suspicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
        title_lower = title.lower()
        
        for pattern in suspicious_patterns:
            if pattern in title_lower:
                raise ValidationError("Title contains invalid characters.")
        
        # Validate that title contains reasonable characters
        if not re.match(r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\(\)\'\"]+$', title):
            raise ValidationError("Title contains invalid characters. Use only letters, numbers, and basic punctuation.")
        
        return escape(title)
    
    def clean_author(self):
        """
        Validate and sanitize author name.
        """
        author = self.cleaned_data.get('author', '').strip()
        
        if not author:
            raise ValidationError("Author is required.")
        
        # Check for minimum length
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")
        
        # Check for suspicious characters
        suspicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
        author_lower = author.lower()
        
        for pattern in suspicious_patterns:
            if pattern in author_lower:
                raise ValidationError("Author name contains invalid characters.")
        
        # Validate that author name contains reasonable characters
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', author):
            raise ValidationError("Author name should contain only letters, spaces, hyphens, periods, and apostrophes.")
        
        return escape(author)
        
    def clean_publication_year(self):
        """
        Validate publication year with enhanced security checks.
        """
        year = self.cleaned_data.get('publication_year')
        
        if year is None:
            raise ValidationError("Publication year is required.")
        
        # Type validation
        if not isinstance(year, int):
            try:
                year = int(year)
            except (ValueError, TypeError):
                raise ValidationError("Publication year must be a valid number.")
        
        # Range validation with current year check
        import datetime
        current_year = datetime.datetime.now().year
        
        if year < 1000:
            raise ValidationError("Publication year cannot be before 1000.")
        
        if year > current_year + 5:
            raise ValidationError(f"Publication year cannot be more than 5 years in the future (max: {current_year + 5}).")
        
        return year
    
    def clean(self):
        """
        Perform cross-field validation and additional security checks.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        
        # Check for duplicate entries (additional business logic validation)
        if title and author:
            existing_book = Book.objects.filter(
                title__iexact=title,
                author__iexact=author
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if existing_book.exists():
                raise ValidationError("A book with this title and author already exists.")
        
        return cleaned_data


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django security best practices.
    This form is used for security demonstration purposes.
    """
    
    title = forms.CharField(
        max_length=200,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book title (2-200 characters)',
            'maxlength': 200,
            'pattern': r'[a-zA-Z0-9\s\-\.\,\:\;\!\?\(\)\'\"]*',
            'title': 'Use only letters, numbers, and basic punctuation'
        }),
        help_text="Input is validated for length, required status, and safe characters"
    )
    
    author = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter author name (2-100 characters)',
            'maxlength': 100,
            'pattern': r'[a-zA-Z\s\-\.\']*',
            'title': 'Only letters, spaces, hyphens, periods, and apostrophes allowed'
        }),
        help_text="Only letters, spaces, hyphens, periods, and apostrophes allowed"
    )
    
    publication_year = forms.IntegerField(
        min_value=1000,
        max_value=2030,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter publication year (1000-2030)',
            'min': 1000,
            'max': 2030
        }),
        help_text="Year validated within reasonable historical range"
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email (optional)'
        }),
        help_text="Email format validation demonstration"
    )
    
    description = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter book description (optional)',
            'rows': 3,
            'maxlength': 500
        }),
        help_text="Optional description with length limit"
    )
    
    def clean_title(self):
        """
        Validate and sanitize title field.
        """
        title = self.cleaned_data.get('title', '').strip()
        
        if not title:
            raise ValidationError("Title is required.")
        
        # Check for suspicious characters that might indicate injection attempts
        suspicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
        title_lower = title.lower()
        
        for pattern in suspicious_patterns:
            if pattern in title_lower:
                raise ValidationError("Title contains invalid characters.")
        
        # Validate that title contains reasonable characters
        if not re.match(r'^[a-zA-Z0-9\s\-\.\,\:\;\!\?\(\)\'\"]+$', title):
            raise ValidationError("Title contains invalid characters. Use only letters, numbers, and basic punctuation.")
        
        return escape(title)
    
    def clean_author(self):
        """
        Validate and sanitize author field.
        """
        author = self.cleaned_data.get('author', '').strip()
        
        if not author:
            raise ValidationError("Author is required.")
        
        # Check for suspicious characters
        suspicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
        author_lower = author.lower()
        
        for pattern in suspicious_patterns:
            if pattern in author_lower:
                raise ValidationError("Author name contains invalid characters.")
        
        # Validate that author name contains reasonable characters
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', author):
            raise ValidationError("Author name should contain only letters, spaces, hyphens, periods, and apostrophes.")
        
        return escape(author)
    
    def clean_description(self):
        """
        Validate and sanitize description field.
        """
        description = self.cleaned_data.get('description', '').strip()
        
        if description:
            # Check for suspicious characters
            suspicious_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'eval(']
            description_lower = description.lower()
            
            for pattern in suspicious_patterns:
                if pattern in description_lower:
                    raise ValidationError("Description contains invalid characters.")
        
        return escape(description) if description else ''
    
    def clean_publication_year(self):
        """
        Validate publication year.
        """
        year = self.cleaned_data.get('publication_year')
        
        if year is None:
            raise ValidationError("Publication year is required.")
        
        # Additional range validation
        import datetime
        current_year = datetime.datetime.now().year
        
        if year > current_year + 5:
            raise ValidationError(f"Publication year cannot be more than 5 years in the future (max: {current_year + 5}).")
        
        return year
