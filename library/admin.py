from django.contrib import admin
from .models import Author, Publisher, Category, LibraryBranch, Staff, Book, Student, IssuedBook, Reservation, Fines


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Настройка админки для авторов"""
    list_display = ('name', 'country', 'date_of_birth', 'book_count')
    search_fields = ('name', 'country')
    ordering = ('name',)
    list_filter = ('country',)

    def book_count(self, obj):
        """Количество книг автора"""
        return obj.books.count()
    book_count.short_description = 'Количество книг'


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Настройка админки для издателей"""
    list_display = ('name', 'contact', 'book_count')
    search_fields = ('name', 'contact')
    ordering = ('name',)

    def book_count(self, obj):
        """Количество книг издателя"""
        return obj.books.count()
    book_count.short_description = 'Количество книг'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка админки для категорий"""
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)

    def book_count(self, obj):
        """Количество книг в категории"""
        return obj.books.count()
    book_count.short_description = 'Количество книг'


@admin.register(LibraryBranch)
class LibraryBranchAdmin(admin.ModelAdmin):
    """Настройка админки для филиалов"""
    list_display = ('name', 'phone', 'address', 'book_count', 'staff_count')
    search_fields = ('name', 'phone')
    ordering = ('name',)

    def book_count(self, obj):
        """Количество книг в филиале"""
        return obj.books.count()
    book_count.short_description = 'Количество книг'

    def staff_count(self, obj):
        """Количество сотрудников в филиале"""
        return obj.staff.count()
    staff_count.short_description = 'Сотрудников'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """Настройка админки для сотрудников"""
    list_display = ('employee_id', 'user', 'position', 'branch', 'phone')
    search_fields = ('employee_id', 'user__username', 'position')
    list_filter = ('position', 'branch')
    ordering = ('employee_id',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Настройка админки для книг"""
    list_display = ('name', 'author', 'publisher', 'category', 'branch', 'isbn')
    list_filter = ('author', 'category', 'publisher', 'branch')
    search_fields = ('name', 'isbn', 'author__name', 'publisher__name')
    ordering = ('name',)
    autocomplete_fields = ['author']

    # Выпадающий список для категории
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all().order_by('name')
        elif db_field.name == "publisher":
            kwargs["queryset"] = Publisher.objects.all().order_by('name')
        elif db_field.name == "branch":
            kwargs["queryset"] = LibraryBranch.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Настройка админки для студентов"""
    list_display = ('user', 'classroom', 'branch', 'roll_no', 'phone')
    list_filter = ('classroom', 'branch')
    search_fields = ('user__username', 'user__email', 'roll_no', 'phone')
    ordering = ('user__username',)


@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    """Настройка админки для выданных книг"""
    list_display = ('book', 'student', 'staff', 'issued_date', 'expiry_date', 'returned')
    list_filter = ('returned', 'issued_date', 'expiry_date', 'staff')
    search_fields = ('book__name', 'student__user__username', 'student__roll_no')
    ordering = ('-issued_date',)
    date_hierarchy = 'issued_date'

    # Выпадающие списки для книги и студента
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.select_related('author').order_by('name')
        elif db_field.name == "student":
            kwargs["queryset"] = Student.objects.select_related('user').order_by('user__username')
        elif db_field.name == "staff":
            kwargs["queryset"] = Staff.objects.select_related('user').order_by('employee_id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Настройка админки для резервирований"""
    list_display = ('student', 'book', 'reservation_date', 'expiry_date', 'status')
    list_filter = ('status', 'reservation_date')
    search_fields = ('student__user__username', 'book__name')
    ordering = ('-reservation_date',)
    date_hierarchy = 'reservation_date'


@admin.register(Fines)
class FinesAdmin(admin.ModelAdmin):
    """Настройка админки для штрафов"""
    list_display = ('student', 'amount', 'reason', 'paid', 'created_date')
    list_filter = ('paid', 'created_date')
    search_fields = ('student__user__username', 'reason')
    ordering = ('-created_date',)
    date_hierarchy = 'created_date'


# Настройка заголовка админ-панели
admin.site.site_header = "Система управления библиотекой"
admin.site.site_title = "Админ-панель библиотеки"
admin.site.index_title = "Добро пожаловать в систему управления библиотекой"
