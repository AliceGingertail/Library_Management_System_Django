from django import forms
from django.contrib.auth.models import User
from . import models

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(
        queryset=models.Book.objects.select_related('author').all(),
        empty_label="Book Name [ISBN]",
        label="Book (Name and ISBN)"
    )
    name2 = forms.ModelChoiceField(
        queryset=models.Student.objects.select_related('user').all(),
        empty_label="Name [Branch] [Class] [Roll No]",
        label="Student Details"
    )

    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class': 'form-control'})
