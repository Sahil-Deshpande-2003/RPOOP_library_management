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
    print(category)
    rooms = Room.objects.filter(category__name = category)
    print(rooms)
    context = {'rooms':rooms}
    return render(request, 'category.html', context)



def displayBooks(request):
    rooms = Room.objects.all()
    context  = {'rooms':rooms}
    return render(request,'display.html',context)

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

def aboutUser(request):
    return render(request,"about.html")

def mathUser(request):
    return render(request,"maths.html")

def addBookUser(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if (form.is_valid):
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'book_form.html',context)

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



