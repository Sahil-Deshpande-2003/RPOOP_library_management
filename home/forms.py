from django.forms import ModelForm
from .models import Room, Category

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields='__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields='__all__'