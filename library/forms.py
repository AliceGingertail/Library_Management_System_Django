from django import forms
from django.contrib.auth.models import User
from . import models


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
        # Делаем некоторые поля необязательными
        self.fields['publisher'].required = False
        self.fields['category'].required = False
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
