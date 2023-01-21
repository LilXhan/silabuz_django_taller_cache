from django import forms 

class BookForm(forms.Form):

    title = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    authors = forms.CharField(max_length=400, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    average_rating = forms.FloatField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    isbn = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    isbn13 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    language_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    num_pages = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    ratings_count = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    text_reviews_count = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    publication_date = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    publisher = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))