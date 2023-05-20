from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from .models import Room, Category
from .forms import RoomForm


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    categories = Category.objects.all()
    context = {"categories" : categories}
    return render(request,'index.html', context)

def categories(request,category):
    rooms = Room.objects.filter(category__name = category)
    context = {'rooms':rooms , 'category':category}
    return render(request, 'category.html', context)

def book(request,book):
    room = Room.objects.get(book_name = book)
    context = {'room':room}
    return render(request, 'book.html', context)

def create_book(request):
    form = RoomForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            book_name = request.POST.get('book_name')
            book_description = request.POST.get('book_description')
            author = request.POST.get('author')
            category = request.POST.get('category')
            image_link = request.POST.get('image_link')
            book_quantity = request.POST.get('book_quantity')
            category_obj = Category.objects.get(name=category)
            room = Room(book_name=book_name, book_description=book_description, author=author, category=category_obj, image_link=image_link, book_quantity=book_quantity)
            room.save()
        except:
            pass
    context = {'form' : form, 'categories':categories }
    return render(request,'create.html',context)

def issue_book(request,book):
    room = Room.objects.get(book_name = book)
    print(room)    
    pass

def UpdateBookUser(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context={}
    return render(request,'room_form.html',context)

def deletebookUser(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('display')
    return render(request,'delete.html',{'obj':room})


def loginUser(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")
