from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required

def index(request):
    books = Book.objects.select_related('author', 'publisher', 'category', 'branch').all()
    return render(request, "index.html", {'books': books})

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        form = forms.BookForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_book.html", {'form': forms.BookForm(), 'alert': alert})
        else:
            return render(request, "add_book.html", {'form': form})
    else:
        form = forms.BookForm()
    return render(request, "add_book.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books})

@login_required(login_url = '/admin_login')
def view_students(request):
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students})

@login_required(login_url = '/admin_login')
def issue_book(request):
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "issue_book.html", {'form': forms.IssueBookForm(), 'alert': alert})
        else:
            return render(request, "issue_book.html", {'form': form})
    else:
        form = forms.IssueBookForm()
    return render(request, "issue_book.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.select_related('book', 'student', 'student__user').all()
    details = []
    for issued in issuedBooks:
        days = (date.today() - issued.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d - 14
            fine = day * 5

        t = (
            issued.student.user,
            issued.student.user_id,
            issued.book.name,
            issued.book.isbn,
            issued.issued_date,
            issued.expiry_date,
            fine,
            issued.id
        )
        details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks': issuedBooks, 'details': details})

@login_required(login_url = '/student_login')
def student_issued_books(request):
    try:
        student = Student.objects.get(user_id=request.user.id)
        issuedBooks = IssuedBook.objects.filter(student=student).select_related('book', 'book__author')
        li1 = []
        li2 = []

        for issued in issuedBooks:
            t = (
                request.user.id,
                request.user.get_full_name,
                issued.book.name,
                issued.book.author.name
            )
            li1.append(t)

            days = (date.today() - issued.issued_date)
            d = days.days
            fine = 0
            if d > 15:
                day = d - 14
                fine = day * 5
            t = (issued.issued_date, issued.expiry_date, fine)
            li2.append(t)
    except Student.DoesNotExist:
        li1 = []
        li2 = []

    return render(request, 'student_issued_books.html', {'li1': li1, 'li2': li2})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html")

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch_id = request.POST.get('branch')
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        # Обрабатываем ForeignKey к LibraryBranch
        if branch_id:
            student.branch = LibraryBranch.objects.get(id=branch_id)
        else:
            student.branch = None
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert, 'branches': LibraryBranch.objects.all()})

    branches = LibraryBranch.objects.all()
    return render(request, "edit_profile.html", {'branches': branches})

def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    students.delete()
    return redirect("/view_students")

def delete_issue(request, myid):
    issued_book = IssuedBook.objects.filter(id=myid)
    issued_book.delete()
    return redirect("/view_issued_book")

def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "change_password.html")

def student_registration(request):
    if request.method == "POST":
        form = forms.StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )

            # Создаем студента
            student = Student.objects.create(
                user=user,
                classroom=form.cleaned_data['classroom'],
                branch=form.cleaned_data.get('branch'),
                roll_no=form.cleaned_data.get('roll_no', ''),
                phone=form.cleaned_data.get('phone', ''),
                image=form.cleaned_data.get('image')
            )

            alert = True
            return render(request, "student_registration.html", {'form': forms.StudentRegistrationForm(), 'alert': alert})
        else:
            return render(request, "student_registration.html", {'form': form})
    else:
        form = forms.StudentRegistrationForm()
    return render(request, "student_registration.html", {'form': form})

def student_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    error = "Вы не студент!"
                    return render(request, "student_login.html", {'form': form, 'error': error})
                else:
                    return redirect("/profile")
            else:
                error = "Неверное имя пользователя или пароль"
                return render(request, "student_login.html", {'form': form, 'error': error})
        else:
            return render(request, "student_login.html", {'form': form})
    else:
        form = forms.LoginForm()
    return render(request, "student_login.html", {'form': form})

def admin_login(request):
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect("/add_book")
                else:
                    error = "Вы не администратор"
                    return render(request, "admin_login.html", {'form': form, 'error': error})
            else:
                error = "Неверное имя пользователя или пароль"
                return render(request, "admin_login.html", {'form': form, 'error': error})
        else:
            return render(request, "admin_login.html", {'form': form})
    else:
        form = forms.LoginForm()
    return render(request, "admin_login.html", {'form': form})

def Logout(request):
    logout(request)
    return redirect ("/")


# Author CRUD
@login_required(login_url = '/admin_login')
def add_author(request):
    if request.method == "POST":
        form = forms.AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_author.html", {'form': forms.AuthorForm(), 'alert': alert})
        else:
            return render(request, "add_author.html", {'form': form})
    else:
        form = forms.AuthorForm()
    return render(request, "add_author.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_authors(request):
    authors = Author.objects.all()
    return render(request, "view_authors.html", {'authors':authors})

@login_required(login_url = '/admin_login')
def delete_author(request, myid):
    author = Author.objects.filter(id=myid)
    author.delete()
    return redirect("/view_authors")


# Publisher CRUD
@login_required(login_url = '/admin_login')
def add_publisher(request):
    if request.method == "POST":
        form = forms.PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_publisher.html", {'form': forms.PublisherForm(), 'alert': alert})
        else:
            return render(request, "add_publisher.html", {'form': form})
    else:
        form = forms.PublisherForm()
    return render(request, "add_publisher.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_publishers(request):
    publishers = Publisher.objects.all()
    return render(request, "view_publishers.html", {'publishers':publishers})

@login_required(login_url = '/admin_login')
def delete_publisher(request, myid):
    publisher = Publisher.objects.filter(id=myid)
    publisher.delete()
    return redirect("/view_publishers")


# Category CRUD
@login_required(login_url = '/admin_login')
def add_category(request):
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_category.html", {'form': forms.CategoryForm(), 'alert': alert})
        else:
            return render(request, "add_category.html", {'form': form})
    else:
        form = forms.CategoryForm()
    return render(request, "add_category.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_categories(request):
    categories = Category.objects.all()
    return render(request, "view_categories.html", {'categories':categories})

@login_required(login_url = '/admin_login')
def delete_category(request, myid):
    category = Category.objects.filter(id=myid)
    category.delete()
    return redirect("/view_categories")


# LibraryBranch CRUD
@login_required(login_url = '/admin_login')
def add_branch(request):
    if request.method == "POST":
        form = forms.LibraryBranchForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_branch.html", {'form': forms.LibraryBranchForm(), 'alert': alert})
        else:
            return render(request, "add_branch.html", {'form': form})
    else:
        form = forms.LibraryBranchForm()
    return render(request, "add_branch.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_branches(request):
    branches = LibraryBranch.objects.all()
    return render(request, "view_branches.html", {'branches':branches})

@login_required(login_url = '/admin_login')
def delete_branch(request, myid):
    branch = LibraryBranch.objects.filter(id=myid)
    branch.delete()
    return redirect("/view_branches")


# Staff CRUD
@login_required(login_url = '/admin_login')
def add_staff(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        employee_id = request.POST['employee_id']
        position = request.POST['position']
        phone = request.POST['phone']
        branch_id = request.POST.get('branch')
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        branch = LibraryBranch.objects.get(id=branch_id) if branch_id else None
        staff = Staff.objects.create(user=user, employee_id=employee_id, position=position, branch=branch, phone=phone)
        user.save()
        staff.save()
        alert = True
        return render(request, "add_staff.html", {'alert':alert, 'branches': LibraryBranch.objects.all()})
    branches = LibraryBranch.objects.all()
    return render(request, "add_staff.html", {'branches': branches})

@login_required(login_url = '/admin_login')
def view_staff(request):
    staff_members = Staff.objects.all()
    return render(request, "view_staff.html", {'staff_members':staff_members})

@login_required(login_url = '/admin_login')
def delete_staff(request, myid):
    staff = Staff.objects.filter(id=myid)
    staff.delete()
    return redirect("/view_staff")


# Reservation CRUD
@login_required(login_url = '/admin_login')
def add_reservation(request):
    if request.method == "POST":
        form = forms.ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_reservation.html", {'form': forms.ReservationForm(), 'alert': alert})
        else:
            return render(request, "add_reservation.html", {'form': form})
    else:
        form = forms.ReservationForm()
    return render(request, "add_reservation.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, "view_reservations.html", {'reservations':reservations})

@login_required(login_url = '/admin_login')
def delete_reservation(request, myid):
    reservation = Reservation.objects.filter(id=myid)
    reservation.delete()
    return redirect("/view_reservations")


# Fines CRUD
@login_required(login_url = '/admin_login')
def add_fine(request):
    if request.method == "POST":
        form = forms.FineForm(request.POST)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "add_fine.html", {'form': forms.FineForm(), 'alert': alert})
        else:
            return render(request, "add_fine.html", {'form': form})
    else:
        form = forms.FineForm()
    return render(request, "add_fine.html", {'form': form})

@login_required(login_url = '/admin_login')
def view_fines(request):
    fines = Fines.objects.all()
    return render(request, "view_fines.html", {'fines':fines})

@login_required(login_url = '/admin_login')
def delete_fine(request, myid):
    fine = Fines.objects.filter(id=myid)
    fine.delete()
    return redirect("/view_fines")

@login_required(login_url = '/admin_login')
def mark_fine_paid(request, myid):
    fine = Fines.objects.get(id=myid)
    fine.paid = True
    fine.save()
    return redirect("/view_fines")