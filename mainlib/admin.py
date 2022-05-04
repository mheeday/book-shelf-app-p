from django import forms
from django.contrib import admin
from .models import Books, UserBook, BookReview


class BookAdmin(admin.ModelAdmin):
    fields = ['book_title', 'book_author', 'book_cat', 'book_desc', 'book_pubd', 'book_image']

admin.site.register(Books, BookAdmin)
admin.site.register(UserBook)
admin.site.register(BookReview)
# Register your models here.
