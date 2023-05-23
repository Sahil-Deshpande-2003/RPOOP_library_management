from django.contrib import admin
from .models import Room, Category, Librarian, Student, Requests
# Register your models here.
admin.site.register(Room)
admin.site.register(Category)
admin.site.register(Librarian)
admin.site.register(Student)
admin.site.register(Requests)