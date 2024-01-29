import uuid
import json

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# book_name,author,id,issue_date

class Category(models.Model): # for book ki categories
    name = models.CharField(max_length=200)
    image_link = models.CharField(max_length=200, null=True) # to set image
    description = models.TextField(null=True)

    def __str__(self):

        return self.name

class Room(models.Model): # used to represent books
    id = models.CharField(max_length=200, primary_key=True)
    book_name = models.CharField(max_length=200)
    book_description = models.TextField(null=True)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT, # used to reference the above category model
        blank=True,
        default=None
    )
    image_link = models.CharField(max_length=200, null=True, default="https://twinklelearning.in/uploads/noimage.jpg")
    book_quantity = models.PositiveSmallIntegerField(blank=True, default=1, null=True)


    def __str__(self):
        return self.book_name
    
class Librarian(models.Model):
    mis = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    issued_books = models.TextField(null=True, blank=True)

    def set_issued_books(self, book_data):
        self.issued_books = json.dumps(book_data) # json to string

    def get_issued_books(self):
        return json.loads(self.issued_books) # string to json
    
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Student(models.Model):
    mis = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    requested_books = models.TextField(null=True, blank=True)
    held_books = models.TextField(null=True, blank=True)

    def set_requested_books(self, book_data):
        self.requested_books = json.dumps(book_data) # The json.dumps function is used to convert the Python list (book_data) into a JSON-formatted string
        # why have u used dumps here??????

    def get_requested_books(self):
        return json.loads(self.requested_books)
    
    def set_held_books(self, book_data):
        self.held_books = json.dumps(book_data)

    def get_held_books(self):
        return json.loads(self.held_books)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Requests(models.Model):
    request_id = models.CharField(max_length=200, primary_key=True, default=uuid.uuid4) # randomly generated

    book_id = models.CharField(max_length=200)
    book_name = models.CharField(max_length=200)
    copies_available = models.PositiveSmallIntegerField(default=1)

    requester_id = models.IntegerField() # MIS
    requester_name = models.CharField(max_length=200)
    request_time = models.CharField(max_length=200, null=True)

    is_issued = models.BooleanField(default=False)
    issuer_id = models.IntegerField(null=True)
    issuer_name = models.CharField(max_length=200, null=True)
    issue_time = models.CharField(max_length=200, null=True)

    is_returned = models.BooleanField(default=False)
    return_time = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.book_name + " - " + str(self.requester_id)