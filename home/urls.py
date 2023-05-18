from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    
    # path('',views.index,name="home"),
    path('', views.index, name="home"),
    path('category/<str:category>/', views.categories, name="category"),
    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),
    path('about',views.aboutUser,name="about"),
    path('maths',views.mathUser,name="maths"),
    path('display',views.displayBooks,name="display"),
    path('addbook',views.addBookUser,name="addbook"),
    path('updatebook/<str:pk>/',views.UpdateBookUser,name="updatebook"),
    path('deletebook/<str:pk>/',views.deletebookUser,name="deletebook"),


]
