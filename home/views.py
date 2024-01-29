import uuid
import datetime
import json

from django.shortcuts import render,redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout,authenticate,login
from .models import Room, Category, Librarian, Student, Requests
from .forms import RoomForm, CategoryForm



# index is for home page

def index(request):
    is_librarian = False

    categories = Category.objects.all()
    context = {"categories" : categories}

    # we check the group for logged in user and if that group matches with the librarian group, is_librarian = True 

    # requests can only be seen by student since student cant enter the if statement

    # user has groups check if it is librarian

    if (request.user.groups.filter(name="Librarian").exists()):
        categories = Category.objects.all()
        # requests are the books not issued
        requests = Requests.objects.filter(is_issued=False)
        # circulating books have been issued but not returned
        circulating_books = Requests.objects.filter(is_returned=False).filter(is_issued=True)
        is_librarian = True
        context = {"categories" : categories, "is_librarian": is_librarian, "requests": requests, "circulating_books": circulating_books}

    return render(request,'index.html', context) # goes to index.html


def categories(request,category): # Fetches rooms (books) based on the selected category 
    rooms = Room.objects.filter(category__name = category)
    context = {'rooms':rooms , 'category':category}
    return render(request, 'category.html', context)

def create_category(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if (request.user.groups.filter(name="Student").exists()): # only librarian has permission
        return redirect("/")

    form = CategoryForm()
    '''
    If any of the required parameters (name, description, image_link) are not present in the POST data, the request.POST.get calls will return None, and trying to create a Category object with None values might raise an exception.
    '''
    if request.method == 'POST': # POST request is used when we have to submit the form
        try:
            name = request.POST.get('book_name')
            description = request.POST.get('book_description')
            image_link = request.POST.get('image_link')
            new_category = Category(name=name, description=description, image_link=image_link)   
            new_category.save()
            return redirect('/')
        except:
            pass
    context = {'form' : form}
    return render(request,'create_category.html',context)


# used to display book

def book(request,pk):
    room = Room.objects.get(id = pk)
    context = {'room':room}
    is_librarian = True
    if not request.user.is_anonymous:
        # logged in already
        if (request.user.groups.filter(name="Librarian").exists()):
            context = {'room':room, "is_librarian": is_librarian}
        else:
            is_held = False # Checks if student has that book
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

            context = {'room':room, "is_requested": is_requested, "is_held": is_held}

    return render(request, 'book.html', context)


def create_book(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if (request.user.groups.filter(name="Student").exists()):
        return redirect("/") # redirect student to main page cause he cant create a book

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
    context = {'form' : form, 'categories':categories } # why to pass categories here
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
    # used to create that object
    new_request.save()

    if (student.requested_books == ""): # executed only once
        requested_books = [
            {
                "id": new_request.book_id,
                "book_name": room.book_name,
                "requester_id": student.mis,
                "requester_name": student.first_name + " " + student.last_name,
                "request_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        ]
        student.set_requested_books(requested_books) # converts array to string
        student.save()
    else:
        # appends requests to the array
        #   This assumes that student.requested_books is a JSON-encoded string
        json_data = json.loads(student.requested_books) # converts string to json format
        json_data.append({
            "id": new_request.book_id,
            "book_name": room.book_name,
            "requester_id": student.mis,
            "requester_name": student.first_name + " " + student.last_name,
            "request_time": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        # So, when you call student.set_requested_books(json_data), it takes a list of dictionaries (json_data), converts it to a JSON string, and sets this string as the value of requested_books for that specific student instance
        # Thoda dekhna ye part!!!!
        student.set_requested_books(json_data)
        student.save()

    return redirect('/book/'+pk)

def cancel_request(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    
    room = Room.objects.get(id=pk)
    student = Student.objects.get(mis=request.user.username)

    requested_books = json.loads(student.requested_books)
    for requested_book in requested_books:
        if (requested_book["id"] == room.id):
            requested_books.remove(requested_book)
            break
    student.set_requested_books(requested_books)
    student.save()
    return redirect('/book/'+pk)

def return_book(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    
    book = Room.objects.get(id=pk)
    student = Student.objects.get(mis=request.user.username)

    held_books = json.loads(student.held_books)
    for held_book in held_books:
        if (held_book["id"] == book.id):
            held_books.remove(held_book)
            break
    student.set_held_books(held_books)
    student.save()

    book.book_quantity = book.book_quantity + 1
    book.save()

    return redirect('/book/'+pk)

def approve_book(request,pk):

    # ONCE MORE!!!!!!!!!!!!!!!

    # here pk is request id and not book_id, hence 1st fetch the request from the request id and from the book_id field of request, fetch the book

    book_request = Requests.objects.get(request_id=pk)
    
    book = Room.objects.get(id = book_request.book_id)
    book.book_quantity = book.book_quantity - 1 # since its issued now
    book.save() # why?

    student = Student.objects.get(mis = book_request.requester_id)
    # request.user.username is a way to retrieve the username of the currently authenticated user in a Django web application
    issuer = Librarian.objects.get(mis=request.user.username) # alloted a MIS to librarian and the found issuer using that MIS

    # remove request from requests object on the student 
    student_requests = json.loads(student.requested_books) # converted the string format to json format so that we can use remove function

    for student_request in student_requests:
        if (student_request["id"] == book_request.book_id):
            student_requests.remove(student_request) # remove the requested book from the student_request array
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
        issuer.set_issued_books(json_data) # again convert json to string because I want to save objects
        issuer.save()


    book_request.is_issued = True
    book_request.issuer_id = issuer.mis
    book_request.issuer_name = issuer.first_name + " " + issuer.last_name
    book_request.issue_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    book_request.save()

    return redirect("/")





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
    original_url = request.META.get('HTTP_REFERER')
    logout(request)
    return redirect(original_url)

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


