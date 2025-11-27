from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Author(models.Model):
    """Модель для авторов книг"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для категорий книг"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """Модель для книг в библиотеке"""
    name = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Автор"
    )
    isbn = models.PositiveIntegerField(verbose_name="ISBN")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books',
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['name']

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'


class Student(models.Model):
    """Модель для студентов"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    classroom = models.CharField(max_length=10, verbose_name="Класс")
    branch = models.CharField(max_length=10, verbose_name="Филиал")
    roll_no = models.CharField(max_length=3, blank=True, verbose_name="Номер")
    phone = models.CharField(max_length=10, blank=True, verbose_name="Телефон")
    image = models.ImageField(upload_to="", blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['user__username']

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'


def expiry():
    return datetime.today() + timedelta(days=14)


class IssuedBook(models.Model):
    """Модель для выданных книг"""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='issued_books',
        verbose_name="Студент"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='issues',
        verbose_name="Книга"
    )
    issued_date = models.DateField(auto_now=True, verbose_name="Дата выдачи")
    expiry_date = models.DateField(default=expiry, verbose_name="Дата возврата")
    returned = models.BooleanField(default=False, verbose_name="Возвращена")

    class Meta:
        verbose_name = "Выданная книга"
        verbose_name_plural = "Выданные книги"
        ordering = ['-issued_date']

    def __str__(self):
        return f"{self.book.name} -> {self.student.user.username}"
