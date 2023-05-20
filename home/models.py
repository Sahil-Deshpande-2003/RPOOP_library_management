from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# book_name,author,id,issue_date

class Category(models.Model):
    name = models.CharField(max_length=200)
    image_link = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)

    def __str__(self):

        return self.name

class Room(models.Model):

    book_name = models.CharField(max_length=200)
    book_description = models.TextField(null=True)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        blank=True,
        default=None
    )
    image_link = models.CharField(max_length=200, null=True, default="https://twinklelearning.in/uploads/noimage.jpg")
    book_quantity = models.PositiveSmallIntegerField(blank=True, default=1, null=True)


    def __str__(self):
        return self.book_name