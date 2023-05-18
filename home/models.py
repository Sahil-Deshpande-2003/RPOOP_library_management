from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# book_name,author,id,issue_date

class Room(models.Model):

    book_name = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_category = models.CharField(max_length=200, default='DEFAULT VALUE')
    book_id = models.IntegerField()
    
    # book_quantity = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    
    book_issue_date = models.CharField(max_length=200,null=True)
 
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:

        ordering = ['-updated','-created']
        

    def __str__(self):

        return self.book_name