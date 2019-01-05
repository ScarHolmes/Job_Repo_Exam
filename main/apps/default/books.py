from django.shortcuts import render, redirect
from .models import User, Book, Author, Review
from django.contrib import messages
import bcrypt


# ---------------------------
#       Login_Success
# ---------------------------

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = request.session['user_id'])
    book = Book.objects.all().order_by('-created_at')
    book_list = [book[0],book[1],book[2]]
    review = Review.objects.all().order_by('-created_at')
    unique_book_id = []
    unique_review = []
    count = 0
    for i in review:
        if i.book.id not in unique_book_id:
            if count < 3:
                unique_book_id.append(i.book.id)
                unique_review.append(i)
                count += 1


    context = { 'user': user[0], 'book':book, 'reviews':unique_review, 'book_list': book_list}
    return render(request, 'logregis/success.html', context)

# ---------------------------
#       Adding_Book
# ---------------------------

def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    author = Author.objects.all()
    print len(author)
    if len(author) <= 1:
        author_name = author[0].name
        context = {'author_name':author_name}
        return render(request, 'logregis/add_book.html', context)
    context = {'authors':author}
    print context
    return render(request, 'logregis/add_book.html', context)

# ---------------------------
#           View Book
# ---------------------------

def view_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.filter(id = book_id)
    if len(book) <= 0:
        return render(request, 'logregis/no_book.html')
    reviews = Review.objects.filter(book__id = book_id).order_by("-created_at")
    if len(reviews) < 1:
        context = {'book':book[0], 'reviews': reviews[0]}
        return render(request, 'logregis/view_book.html', context)

    context = {'book':book[0], 'reviews': reviews}
    return render(request, 'logregis/view_book.html', context)

# ---------------------------
#           View User
# ---------------------------

def view_user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id = user_id)
    if len(user) <= 0:
        return render(request, 'logregis/no_user.html')
    print user
    reviews = Review.objects.filter(user__id = user_id)

    books = Review.objects.filter(user__id = user_id)
    book_list = []
    for books in books:
        if books.book not in book_list:
            book_list.append(books.book)

    print book_list
    context = {'user':user[0], 'total_reviews': len(reviews), 'book_list': book_list}

    return render(request, 'logregis/view_user.html', context)

# ---------------------------
#       Registration
# ---------------------------

def registration(request):
    if 'user_id' in request.session:
        return redirect('/success')

    if request.method == 'POST':
        reg_data = User.objects.reg_validator(request.POST)
        if reg_data[0]:
            request.session['user_id'] = reg_data[1].id
            return redirect('/success')

        for error in reg_data[1]:
            messages.add_message(request, messages.INFO ,error)
    return redirect('/register')


# ---------------------------
#        Adding_Book
# ---------------------------

def adding_book(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        user_id = request.session['user_id']
        B = Book.objects.adding_book(request.POST, user_id)
        if not B[0]:
            for error in B[1]:
                messages.add_message(request, messages.INFO ,error)
            return redirect('/add_book')

        return redirect('book')
    return redirect('/add_book')

# ---------------------------
#        Adding Review
# ---------------------------

def adding_review(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        user_id = request.session['user_id']
        B = Review.objects.adding_review(book_id, user_id, request.POST)
        for error in B1[1]:
            messages.add_message(request, messages.INFO ,error)
        return redirect('/books/{}'.format(book_id))


        if not validEmail:
            errors['email'] = "Enter a valid email address"

            for key,value in errors.items():
            messages.error(request, value)
        return redirect('/users')
# ---------------------------
#        Remove Review
# ---------------------------

def deleteprocess(request, id):
    User.objects.get(id=id).delete()
    return redirect("/users")
# ---------------------------
#        Edit Review
# ---------------------------

def edit(request, id):
this_user = users.objects.get(id = str(id))
print('EDIT::',this_user)
context = {'ID' : this_user.id,
            'fname' : this_user.fname,
            'lname' : this_user.lname,
            'email' : this_user.email,
            'created_at' : this_user.created_at}
return render(request, "edit_user.html", context)

# ---------------------------------------
#                 Modle INFO
# --------------------------------------
class ReviewManager(models.Manager):
    def adding_review(self, book_id, user_id, POST):
        error_list = []
        if POST['review'] == "":
            error_list.append("Review cannot be Blank")
            return False, error_list
        U1 = User.objects.get(id = user_id)
        B1 = Book.objects.get(id = book_id)
        Review.objects.create(review = POST['review'], ratings = POST['ratings'], user = U1, book = B1)
        error_list.append("Review added Successfully")
        return True, error_list
# ---------------------------------------
#                 URL INFO 
# --------------------------------------
from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$',views.index), 
    url(r'^display$', views.index),
    url(r'^newdisplay$', views.new),
    url(r'^create$', views.create),
    url(r'^[0-9]{2}/edit$', views.show), 
    url(r'^[0-9]{2}/delete$', views.destroy)

# ---------------------------------------
#                 URL/View Follow  INFO 
# --------------------------------------

from django.shortcuts import render, HttpResponse, redirect
# the index function is called when root is visited
def index(request):
    response = "placeholder for blog"
    return HttpResponse(response)

def new(request):
    response = "placeholder to display a new form to create a new blog"
    return HttpResponse(response)

def create(request):
    return redirect('/')
def show(request):
    response = "Placeholder to display" + str(request)
    return HttpResponse(response)

def destroy(request):
    return redirect('/')
# ---------------------------------------
#                 Data base ONFO
# --------------------------------------

# Create 3 different user accounts
User.objects.create(first_name="Hoho", last_name = "Hoho", email = "Hoho@gmail.com")
User.objects.create(first_name="Huhu", last_name = "Huhu", email = "Huhu@gmail.com")
User.objects.create(first_name="Haha", last_name = "Haha", email = "Haha@gmail.com")

# Have the first user create/upload 2 books.
Book.objects.create(name="Booke1", desc="Booke1 description", uploader=User.objects.get(id=1))
Book.objects.create(name="Booke2", desc="Booke2 description", uploader=User.objects.get(id=1))

# Have the second user create/upload 2 other books.
Book.objects.create(name="Booke3", desc="Booke3 description", uploader=User.objects.get(id=2))
Book.objects.create(name="Booke4", desc="Booke4 description", uploader=User.objects.get(id=2))

# Have the third user create/upload 2 other books.
Book.objects.create(name="Booke5", desc="Booke5 description", uploader=User.objects.get(id=3))
Book.objects.create(name="Booke6", desc="Booke6 description", uploader=User.objects.get(id=3))

# Have the first user like the last book and the first book
a = Book.objects.first()
b = Book.objects.last()
c = User.objects.first()
a.liked_users.add(c)
b.liked_users.add(c)
a.save()
b.save()

# Have the second user like the first book and the third book
a = Book.objects.first()
b = Book.objects.get(id=3)
c = User.objects.get(id=2)
a.liked_users.add(c)
b.liked_users.add(c)
a.save()
b.save()

# Have the third user like all books
a = Book.objects.get(id=1)
b = Book.objects.get(id=2)
c = Book.objects.get(id=3)
d = Book.objects.get(id=4)
e = Book.objects.get(id=5)
f = Book.objects.get(id=6)
g = User.objects.get(id=3)
a.liked_users.add(g)
b.liked_users.add(g)
c.liked_users.add(g)
d.liked_users.add(g)
e.liked_users.add(g)
f.liked_users.add(g)
a.save()
b.save()
c.save()
d.save()
e.save()
f.save()

# Display all users who like the first book
Book.objects.first().liked_users.all()

# Display the user who uploaded the first book
Book.objects.first().uploader

# Display all users who like the second book
Book.objects.get(id=2).liked_users.all()

# Display the user who uploaded the second book
Book.objects.get(id=2).uploader