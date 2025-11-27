"""
Скрипт для заполнения базы данных начальными данными
Script to populate database with initial data

Запуск / Run:
python populate_db.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSystem.settings')
django.setup()

from library.models import Author, Category, Book
from django.contrib.auth.models import User

def populate():
    print("Начало заполнения базы данных / Starting database population...")

    # Создание авторов / Create authors
    authors_data = [
        {"name": "Лев Толстой", "bio": "Русский писатель, автор романов 'Война и мир' и 'Анна Каренина'"},
        {"name": "Фёдор Достоевский", "bio": "Русский писатель, автор романов 'Преступление и наказание' и 'Братья Карамазовы'"},
        {"name": "Alexander Pushkin", "bio": "Russian poet, playwright, and novelist"},
        {"name": "J.K. Rowling", "bio": "British author, best known for Harry Potter series"},
        {"name": "George Orwell", "bio": "English novelist and essayist, author of '1984' and 'Animal Farm'"},
    ]

    authors = []
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            name=author_data["name"],
            defaults={"bio": author_data["bio"]}
        )
        authors.append(author)
        if created:
            print(f"✓ Создан автор / Author created: {author.name}")
        else:
            print(f"- Автор уже существует / Author already exists: {author.name}")

    # Создание категорий / Create categories
    categories_data = [
        {"name": "Классическая литература", "description": "Произведения классиков мировой литературы"},
        {"name": "Фантастика", "description": "Научная фантастика и фэнтези"},
        {"name": "Детективы", "description": "Детективные романы и триллеры"},
        {"name": "Поэзия", "description": "Сборники стихов и поэм"},
        {"name": "Научная литература", "description": "Научно-популярные книги"},
    ]

    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories.append(category)
        if created:
            print(f"✓ Создана категория / Category created: {category.name}")
        else:
            print(f"- Категория уже существует / Category already exists: {category.name}")

    # Создание книг / Create books
    books_data = [
        {"name": "Война и мир", "author": 0, "isbn": 9785170123456, "category": 0},
        {"name": "Анна Каренина", "author": 0, "isbn": 9785170123457, "category": 0},
        {"name": "Преступление и наказание", "author": 1, "isbn": 9785170123458, "category": 0},
        {"name": "Братья Карамазовы", "author": 1, "isbn": 9785170123459, "category": 0},
        {"name": "Евгений Онегин", "author": 2, "isbn": 9785170123460, "category": 3},
        {"name": "Harry Potter and the Philosopher's Stone", "author": 3, "isbn": 9780747532699, "category": 1},
        {"name": "1984", "author": 4, "isbn": 9780451524935, "category": 1},
        {"name": "Animal Farm", "author": 4, "isbn": 9780451526342, "category": 0},
    ]

    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            isbn=book_data["isbn"],
            defaults={
                "name": book_data["name"],
                "author": authors[book_data["author"]],
                "category": categories[book_data["category"]]
            }
        )
        if created:
            print(f"✓ Создана книга / Book created: {book.name}")
        else:
            print(f"- Книга уже существует / Book already exists: {book.name}")

    print("\n✅ Заполнение базы данных завершено! / Database population completed!")
    print(f"Авторов / Authors: {Author.objects.count()}")
    print(f"Категорий / Categories: {Category.objects.count()}")
    print(f"Книг / Books: {Book.objects.count()}")

if __name__ == '__main__':
    populate()
