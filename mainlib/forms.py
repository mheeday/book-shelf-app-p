from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BookReview, Books

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta: 
        model = BookReview
        fields = ('rev',)

class BookForm(forms.ModelForm):
    image_file = forms.ImageField()
    class Meta:
        model = Books
        fields = ('book_title', 'book_author', 'book_cat', 'book_desc', 'book_pubd', 'image_file')