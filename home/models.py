from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# book_name,author,id,issue_date

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):

        return self.name

class Room(models.Model):

    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        default=None
    )

    def __str__(self):
        return self.book_name