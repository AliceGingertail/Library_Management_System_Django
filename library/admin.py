from django.contrib import admin
from .models import Author, Category, Book, Student, IssuedBook


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Настройка админки для авторов"""
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)

    def book_count(self, obj):
        """Количество книг автора"""
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


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Настройка админки для книг"""
    list_display = ('name', 'author', 'category', 'isbn')
    list_filter = ('author', 'category')
    search_fields = ('name', 'isbn', 'author__name')
    ordering = ('name',)
    autocomplete_fields = ['author']

    # Выпадающий список для категории
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all().order_by('name')
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
    list_display = ('book', 'student', 'issued_date', 'expiry_date', 'returned')
    list_filter = ('returned', 'issued_date', 'expiry_date')
    search_fields = ('book__name', 'student__user__username', 'student__roll_no')
    ordering = ('-issued_date',)
    date_hierarchy = 'issued_date'

    # Выпадающие списки для книги и студента
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "book":
            kwargs["queryset"] = Book.objects.select_related('author').order_by('name')
        elif db_field.name == "student":
            kwargs["queryset"] = Student.objects.select_related('user').order_by('user__username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Настройка заголовка админ-панели
admin.site.site_header = "Система управления библиотекой"
admin.site.site_title = "Админ-панель библиотеки"
admin.site.index_title = "Добро пожаловать в систему управления библиотекой"