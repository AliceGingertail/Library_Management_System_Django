from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Author(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class LibraryBranch(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Library Branches"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    branch = models.ForeignKey(LibraryBranch, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"

    class Meta:
        verbose_name_plural = "Staff"


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)  # Старое поле, оставлено для совместимости
    author_fk = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)  # Старое поле
    category_fk = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    branch = models.ForeignKey(LibraryBranch, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="", blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'


def expiry():
    return datetime.today() + timedelta(days=14)


class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)  # Старое поле
    student_fk = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='issued_books')
    isbn = models.CharField(max_length=13)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_records')
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='issued_books')
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.isbn} - {self.student_id}"


class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    expiry_date = models.DateField(default=expiry)

    def __str__(self):
        return f"{self.student.user.username} - {self.book.name} - {self.status}"


class Fines(models.Model):
    issued_book = models.ForeignKey(IssuedBook, on_delete=models.CASCADE, related_name='fines')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    paid = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - ₹{self.amount} - {'Paid' if self.paid else 'Unpaid'}"

    class Meta:
        verbose_name_plural = "Fines"
