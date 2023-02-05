from tkinter import CASCADE

from django.db import models
from knox.models import User



# Create your models here.

class Book(models.Model):
    choice = [('fantasy', 'Fantasy'),
              ('romance', 'Romance'),
              ('science_fiction', 'Science Fiction'),
              ('education', 'Education'),
              ('psychology', 'Psychology'),
              ('motivation_inspiration', 'Motivation & Inspiration'),

              ]

    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=6,decimal_places=2, null=True)
    content = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='photos/%y/%m/%d', null=True)
    active = models.BooleanField(default=True)
    category = models.CharField(max_length=50, null=True, choices=choice)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book_id_id= models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id_id= models.ForeignKey(User, on_delete=models.CASCADE)
    reviewContent=models.TextField(null=False, blank=True)
    # bookDetail = models.ArrayField(
    #     model_container=Book,
    # )

