from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    
    # path('',views.index,name="home"),
    path('', views.index, name="home"),
    path('category/<str:category>/', views.categories, name="category"),

    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),

    path('book/<str:book>/', views.book, name="book"),
    path('issue/<str:book>/', views.issue_book, name="issue"),
    path('create',views.create_book,name="addbook"),
    path('updatebook/<str:pk>/',views.UpdateBookUser,name="updatebook"),
    path('deletebook/<str:pk>/',views.deletebookUser,name="deletebook"),


]
