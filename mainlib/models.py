from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# Create your models here.
class Books(models.Model):
    BOOK_CATEGORIES = [
        ('Comic', 'Comic'),
        ('Fantasy', 'Fantasy'),
        ('Action', 'Action'),
        ('Thriller', 'Thriller'),
        ('Contemporary', 'Contemporary'),
    ]
    book_title = models.CharField('Title', max_length=200)
    book_author = models.CharField('Author', max_length=200)
    book_cat = models.CharField('Category', max_length=15, choices=BOOK_CATEGORIES)
    book_cover = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    book_img_url = models.CharField(max_length=200)
    book_desc = models.CharField('About the Book', max_length=200)
    book_pubd = models.DateField('Publication Date')
    book_image = models.ImageField(upload_to=settings.MEDIA_ROOT)

    def save(self, *args, **kwargs):
        if not self.book_img_url:
            self.book_img_url = f"/media/{self.book_cover}.jpg"
            self.book_image.name = f"{self.book_cover}.jpg"
            super(Books, self).save(*args, **kwargs)
    

class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField()
    archived = models.BooleanField(default=False)

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    rev = models.CharField(max_length=1000)
    date_posted = models.DateTimeField()