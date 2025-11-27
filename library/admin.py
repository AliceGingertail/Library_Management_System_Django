from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(LibraryBranch)
admin.site.register(Staff)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(IssuedBook)
admin.site.register(Reservation)
admin.site.register(Fines)