import uuid
import datetime
import json

from django.shortcuts import render,redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout,authenticate,login
from .models import Room, Category, Librarian, Student, Requests
from .forms import RoomForm



def index(request):
    is_librarian = False

    categories = Category.objects.all()
    context = {"categories" : categories}

    if (request.user.groups.filter(name="Librarian").exists()):
        categories = Category.objects.all()
        requests = Requests.objects.filter(is_issued=False)
        is_librarian = True
        context = {"categories" : categories, "is_librarian": is_librarian, "requests": requests}

    return render(request,'index.html', context)


def categories(request,category):
    rooms = Room.objects.filter(category__name = category)
    context = {'rooms':rooms , 'category':category}
    return render(request, 'category.html', context)


def book(request,pk):
    room = Room.objects.get(id = pk)
    is_librarian = True
    if (request.user.groups.filter(name="Librarian").exists()):
        context = {'room':room, "is_librarian": is_librarian}
    else:
        is_held = False
        is_requested = False
        student = Student.objects.get(mis=request.user.username)

        if (student.held_books != ""):
            held_books = json.loads(student.held_books)
            for book in held_books:
                if (book["id"] == room.id):
                    is_held = True
                    break

        if (student.requested_books != ""):
            requested_books = json.loads(student.requested_books)
            for book in requested_books:
                if (book["id"] == room.id):
                    is_requested = True
                    break

        print(is_held, is_requested)

        context = {'room':room, "is_requested": is_requested, "is_held": is_held}

    return render(request, 'book.html', context)


def create_book(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if (request.user.groups.filter(name="Student").exists()):
        return redirect("/")

    form = RoomForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            id = uuid.uuid4()
            book_name = request.POST.get('book_name')
            book_description = request.POST.get('book_description')
            author = request.POST.get('author')
            category = request.POST.get('category')
            image_link = request.POST.get('image_link')
            book_quantity = request.POST.get('book_quantity')
            category_obj = Category.objects.get(name=category)
            room = Room(id=id, book_name=book_name, book_description=book_description, author=author, category=category_obj, image_link=image_link, book_quantity=book_quantity)
            room.save()
        except:
            pass
    context = {'form' : form, 'categories':categories }
    return render(request,'create.html',context)

def request_book(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    
    room = Room.objects.get(id=pk)
    student = Student.objects.get(mis=request.user.username)

    new_request = Requests(
        book_id = room.id,
        book_name = room.book_name,
        copies_available = room.book_quantity,

        requester_id = student.mis,
        requester_name = student.first_name + " " + student.last_name,
        request_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    )
    new_request.save()

    if (student.requested_books == ""):
        requested_books = [
            {
                "id": room.id,
                "book_name": room.book_name,
                "requester_id": student.mis,
                "requester_name": student.first_name + " " + student.last_name,
                "request_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        ]
        student.set_requested_books(requested_books)
        student.save()
    else:
        json_data = json.loads(student.requested_books)
        json_data.append({
            "id": room.id,
            "book_name": room.book_name,
            "requester_id": student.mis,
            "requester_name": student.first_name + " " + student.last_name,
            "request_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        student.set_requested_books(json_data)
        student.save()

    return redirect('/book/'+pk)



def approve_book(request,pk):
    book_request = Requests.objects.get(request_id=pk)
    
    book = Room.objects.get(id = book_request.book_id)
    book.book_quantity = book.book_quantity - 1
    book.save()

    student = Student.objects.get(mis = book_request.requester_id)
    issuer = Librarian.objects.get(mis=request.user.username)

    student_requests = json.loads(student.requested_books)
    for student_request in student_requests:
        if (student_request["id"] == book_request.book_id):
            student_requests.remove(student_request)
            break
    student.set_requested_books(student_requests)
    student.save()

    if (student.held_books == ""):
        new_held_book = [
            {
                "id": book.id,
                "book_name": book.book_name,
                "issuer_id": issuer.mis,
                "issuer_name": issuer.first_name + " " + issuer.last_name,
                "issue_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        ]
        student.set_held_books(new_held_book)
        student.save()
    else:
        json_data = json.loads(student.held_books)
        json_data.append({
            "id": book.id,
            "book_name": book.book_name,
            "issuer_id": issuer.mis,
            "issuer_name": issuer.first_name + " " + issuer.last_name,
            "issue_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        student.set_held_books(json_data)
        student.save()

    if (issuer.issued_books == ""):
        new_issued_book = [
            {
                "id": book.id,
                "book_name": book.book_name,
                "student_id": student.mis,
                "student_name": student.first_name + " " + student.last_name,
                "issue_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        ]
        issuer.set_issued_books(new_issued_book)
        issuer.save()
    else:
        json_data = json.loads(issuer.issued_books)
        json_data.append({
            "id": book.id,
            "book_name": book.book_name,
            "student_id": student.mis,
            "student_name": student.first_name + " " + student.last_name,
            "issue_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        issuer.set_issued_books(json_data)
        issuer.save()


    book_request.is_issued = True
    book_request.issuer_id = issuer.mis
    book_request.issuer_name = issuer.first_name + " " + issuer.last_name
    book_request.issue_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    book_request.save()

    return redirect("/")


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


def user(request,pk):
    user = User.objects.get(username=pk)
    if (user.groups.filter(name="Librarian").exists()):
        librarian = Librarian.objects.get(mis=pk)
        if (librarian.requested_books == ""):
            context = {"user": librarian}
        else:
            requested_books = json.loads(librarian.requested_books)
            context = {"user": librarian, "requested_books": requested_books}
    else:
        student = Student.objects.get(mis=pk)
        if (student.requested_books == ""):
            context = {"user": student}
        else:
            requested_books = json.loads(student.requested_books)
            context = {"user": student, "requested_books": requested_books}
    return render(request,'user.html',context)

def createUser(request):
    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect("/login")
        except:
            return redirect("/user/create")
    return render(request,'createuser.html')
