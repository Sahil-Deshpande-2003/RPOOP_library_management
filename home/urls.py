from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    
    # path('',views.index,name="home"),
    path('', views.index, name="home"),
    path('category/<str:category>/', views.categories, name="category"),

    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),

    path('user/<str:pk>/', views.user, name="user"),
    path('/user/create',views.createUser,name="createuser"),

    path('book/<str:pk>/', views.book, name="book"),
    path('book/create',views.create_book,name="addbook"),
    path('request/<str:pk>/', views.request_book, name="request"),
    

    path('book/approve/<str:pk>/', views.approve_book, name="approve"),

    path('updatebook/<str:pk>/',views.UpdateBookUser,name="updatebook"),
    path('deletebook/<str:pk>/',views.deletebookUser,name="deletebook"),


]
