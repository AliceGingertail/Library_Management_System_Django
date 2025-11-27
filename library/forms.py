from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator
from . import models
import re


class BookForm(forms.ModelForm):
    """Форма для добавления/редактирования книги"""
    class Meta:
        model = models.Book
        fields = ['name', 'author', 'publisher', 'isbn', 'category', 'branch']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название книги'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ISBN'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название книги',
            'author': 'Автор',
            'publisher': 'Издатель',
            'isbn': 'ISBN',
            'category': 'Категория',
            'branch': 'Филиал',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publisher'].required = False
        self.fields['category'].required = False
        self.fields['branch'].required = False


class StudentRegistrationForm(forms.ModelForm):
    """Форма для регистрации студента с валидацией"""
    username = forms.CharField(
        max_length=150,
        validators=[MinLengthValidator(3, 'Имя пользователя должно содержать минимум 3 символа')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
        label='Имя пользователя'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
        label='Фамилия'
    )
    email = forms.EmailField(
        validators=[EmailValidator('Введите корректный email адрес')],
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'}),
        label='Email'
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Минимум 8 символов'}),
        label='Пароль',
        help_text='Пароль должен содержать минимум 8 символов, букву и цифру'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        label='Подтверждение пароля'
    )

    class Meta:
        model = models.Student
        fields = ['classroom', 'branch', 'roll_no', 'phone', 'image']
        widgets = {
            'classroom': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Выберите класс'),
                ('1', '1 класс'),
                ('2', '2 класс'),
                ('3', '3 класс'),
                ('4', '4 класс'),
                ('5', '5 класс'),
                ('6', '6 класс'),
                ('7', '7 класс'),
                ('8', '8 класс'),
                ('9', '9 класс'),
                ('10', '10 класс'),
                ('11', '11 класс'),
            ]),
            'branch': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Выберите филиал'),
                ('Главный', 'Главный филиал'),
                ('Центральный', 'Центральный филиал'),
                ('Северный', 'Северный филиал'),
                ('Южный', 'Южный филиал'),
            ]),
            'roll_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (___) ___-__-__'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'classroom': 'Класс',
            'branch': 'Филиал',
            'roll_no': 'Номер',
            'phone': 'Телефон',
            'image': 'Фото студента',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Убираем лишние символы
        cleaned_phone = phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
        # Проверка на корректность телефона (только цифры и +, от 10 до 15 символов)
        if not re.match(r'^\+?\d{10,15}$', cleaned_phone):
            raise ValidationError('Введите корректный номер телефона (10-15 цифр)')
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Пароли не совпадают')

            # Проверка сложности пароля
            if len(password) < 8:
                raise ValidationError('Пароль должен содержать минимум 8 символов')
            if not re.search(r'[A-Za-z]', password):
                raise ValidationError('Пароль должен содержать хотя бы одну букву')
            if not re.search(r'\d', password):
                raise ValidationError('Пароль должен содержать хотя бы одну цифру')

        return cleaned_data


class AuthorForm(forms.ModelForm):
    """Форма для добавления/редактирования автора"""
    class Meta:
        model = models.Author
        fields = ['name', 'date_of_birth', 'country', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя автора'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Биография'}),
        }
        labels = {
            'name': 'Имя автора',
            'date_of_birth': 'Дата рождения',
            'country': 'Страна',
            'bio': 'Биография',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False
        self.fields['bio'].required = False


class PublisherForm(forms.ModelForm):
    """Форма для добавления/редактирования издателя"""
    class Meta:
        model = models.Publisher
        fields = ['name', 'address', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название издательства'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Адрес'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный телефон или email'}),
        }
        labels = {
            'name': 'Название издательства',
            'address': 'Адрес',
            'contact': 'Контакт',
        }


class CategoryForm(forms.ModelForm):
    """Форма для добавления/редактирования категории"""
    class Meta:
        model = models.Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Описание категории'}),
        }
        labels = {
            'name': 'Название категории',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class LibraryBranchForm(forms.ModelForm):
    """Форма для добавления/редактирования филиала библиотеки"""
    class Meta:
        model = models.LibraryBranch
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название филиала'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Адрес филиала'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }
        labels = {
            'name': 'Название филиала',
            'address': 'Адрес',
            'phone': 'Телефон',
        }


class StaffForm(forms.ModelForm):
    """Форма для добавления/редактирования сотрудника"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        label='Имя пользователя'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
        label='Фамилия'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )

    class Meta:
        model = models.Staff
        fields = ['employee_id', 'position', 'branch', 'phone']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID сотрудника'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Должность'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        }
        labels = {
            'employee_id': 'ID сотрудника',
            'position': 'Должность',
            'branch': 'Филиал',
            'phone': 'Телефон',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].required = False


class IssueBookForm(forms.ModelForm):
    """Форма для выдачи книги"""
    class Meta:
        model = models.IssuedBook
        fields = ['student', 'book', 'staff']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
            'staff': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student': 'Студент',
            'book': 'Книга',
            'staff': 'Сотрудник (опционально)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].required = False
        # Оптимизируем запросы с select_related
        self.fields['book'].queryset = models.Book.objects.select_related('author').all()
        self.fields['student'].queryset = models.Student.objects.select_related('user').all()


class ReservationForm(forms.ModelForm):
    """Форма для резервирования книги"""
    class Meta:
        model = models.Reservation
        fields = ['student', 'book']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student': 'Студент',
            'book': 'Книга',
        }


class FineForm(forms.ModelForm):
    """Форма для добавления штрафа"""
    class Meta:
        model = models.Fines
        fields = ['issued_book', 'student', 'amount', 'reason']
        widgets = {
            'issued_book': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'issued_book': 'Выданная книга',
            'student': 'Студент',
            'amount': 'Сумма штрафа',
            'reason': 'Причина',
        }


class LoginForm(forms.Form):
    """Форма для входа"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )
