from django.contrib import admin
from django.urls import path,include
from home import views
'''
path('user/<str:pk>/', views.user, name="user")
        # used in
<a href="/user/{{request.requester_id}}">
                      {{book.requester_name}}
                    </a>
                    in index.html ???
            '''

'''
 path('request/cancel/<str:pk>/', views.cancel_request, name="cancel_request")
 used in book.html
<a href="{% url 'cancel_request' room.id %}">

'''
     
'''

path('book/<str:pk>/', views.book, name="book")
used in 

<a href="{% url 'book' room.id %}" style="text-decoration: none;"> in category.html
'''

urlpatterns = [
    

    path('', views.index, name="home"), # used

    path('login',views.loginUser,name="login"), # used
    path('logout',views.logoutUser,name="logout"), # used

    path('user/<str:pk>/', views.user, name="user"), # used? see top
                  
    path('category/<str:category>/', views.categories, name="category"), # used
    path('category/create',views.create_category,name="addcategory"),  # used

    path('book/<str:pk>/', views.book, name="book"), # used
    path('book/create',views.create_book,name="addbook"), # used

    path('request/<str:pk>/', views.request_book, name="request"), # used
    path('request/cancel/<str:pk>/', views.cancel_request, name="cancel_request"), # used 
    path('return/<str:pk>/', views.return_book, name="return"),  # used 

    path('book/approve/<str:pk>/', views.approve_book, name="approve"), # used



]
