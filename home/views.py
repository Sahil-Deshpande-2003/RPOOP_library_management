from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from .models import Room
from .forms import RoomForm
# rooms=[

#     {'id':1,'name':'Sahil'},
#     {'id':2,'name':'Manas'},
#     {'id':3,'name':'Mamta'},
# ]


# Create your views here.

# orignal wala comment out hai

def index(request):

    if request.user.is_anonymous:

        return redirect("/login")
    
  
    rooms = Room.objects.values('book_category').distinct()

    

    context  = {'rooms':rooms}

    return render(request,'index.html',context)
    # return render(request,'display.html')

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
    # return redirect("/maths")



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



def categorybookUser(request,pk):

    # rooms = Room.objects.all()
    rooms = Room.objects.get(book_category = pk)

    # room = None

    # for i in rooms:

        

    #         room = i
        
    context = {'rooms':rooms}

    # return render(request,'display.html',context)
    return render(request,'category.html',context)





# Harry$$$***000