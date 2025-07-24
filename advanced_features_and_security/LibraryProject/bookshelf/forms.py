from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year'
            }),
        }
        
    def clean_publication_year(self):
        """
        Validate that publication year is reasonable.
        """
        year = self.cleaned_data['publication_year']
        if year < 1000 or year > 2030:
            raise forms.ValidationError("Publication year must be between 1000 and 2030.")
        return year
