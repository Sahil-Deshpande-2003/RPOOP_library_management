from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    
    # path('',views.index,name="home"),
    path('', views.index, name="home"),

    path('login',views.loginUser,name="login"),
    path('logout',views.logoutUser,name="logout"),

    path('user/<str:pk>/', views.user, name="user"),
    path('/user/create',views.createUser,name="createuser"),

    path('category/<str:category>/', views.categories, name="category"),
    path('category/create',views.create_category,name="addcategory"),

    path('book/<str:pk>/', views.book, name="book"),
    path('book/create',views.create_book,name="addbook"),

    path('request/<str:pk>/', views.request_book, name="request"),
    path('request/cancel/<str:pk>/', views.cancel_request, name="cancel_request"),
    path('return/<str:pk>/', views.return_book, name="return"),

    path('book/approve/<str:pk>/', views.approve_book, name="approve"),

    path('updatebook/<str:pk>/',views.UpdateBookUser,name="updatebook"),
    path('deletebook/<str:pk>/',views.deletebookUser,name="deletebook"),


]
