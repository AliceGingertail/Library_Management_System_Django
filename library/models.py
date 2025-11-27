from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Author(models.Model):
    """Модель для авторов книг"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Имя автора")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    country = models.CharField(max_length=100, verbose_name="Страна")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    """Модель для издателей"""
    name = models.CharField(max_length=200, verbose_name="Название издательства")
    address = models.TextField(verbose_name="Адрес")
    contact = models.CharField(max_length=100, verbose_name="Контакт")

    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"
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


class LibraryBranch(models.Model):
    """Модель для филиалов библиотеки"""
    name = models.CharField(max_length=200, verbose_name="Название филиала")
    address = models.TextField(verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Филиал библиотеки"
        verbose_name_plural = "Филиалы библиотеки"
        ordering = ['name']

    def __str__(self):
        return self.name


class Staff(models.Model):
    """Модель для сотрудников библиотеки"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="ID сотрудника")
    position = models.CharField(max_length=100, verbose_name="Должность")
    branch = models.ForeignKey(LibraryBranch, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='staff', verbose_name="Филиал")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"


class Book(models.Model):
    """Модель для книг в библиотеке"""
    name = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name="Автор"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Издатель"
    )
    isbn = models.PositiveIntegerField(verbose_name="ISBN")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books',
        verbose_name="Категория"
    )
    branch = models.ForeignKey(
        LibraryBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name="Филиал"
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
    branch = models.ForeignKey(
        LibraryBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Филиал"
    )
    roll_no = models.CharField(max_length=3, blank=True, verbose_name="Номер")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    image = models.ImageField(upload_to="students/", blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['user__username']

    def __str__(self):
        branch_name = self.branch.name if self.branch else "Без филиала"
        return str(self.user) + " ["+branch_name+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'


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
    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_books',
        verbose_name="Сотрудник"
    )
    returned = models.BooleanField(default=False, verbose_name="Возвращена")

    class Meta:
        verbose_name = "Выданная книга"
        verbose_name_plural = "Выданные книги"
        ordering = ['-issued_date']

    def __str__(self):
        return f"{self.book.name} -> {self.student.user.username}"


class Reservation(models.Model):
    """Модель для резервирования книг"""
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Студент"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="Книга"
    )
    reservation_date = models.DateField(auto_now_add=True, verbose_name="Дата резервирования")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидает'),
        ('fulfilled', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ], default='pending', verbose_name="Статус")
    expiry_date = models.DateField(default=expiry, verbose_name="Срок действия")

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"
        ordering = ['-reservation_date']

    def __str__(self):
        return f"{self.student.user.username} - {self.book.name} - {self.status}"


class Fines(models.Model):
    """Модель для штрафов"""
    issued_book = models.ForeignKey(
        IssuedBook,
        on_delete=models.CASCADE,
        related_name='fines',
        verbose_name="Выданная книга"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='fines',
        verbose_name="Студент"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    reason = models.TextField(verbose_name="Причина")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Штраф"
        verbose_name_plural = "Штрафы"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.student.user.username} - ₹{self.amount} - {'Оплачено' if self.paid else 'Не оплачено'}"
