# Library Management System using Python on Django Framework

### О проекте / About the Project

**Система управления библиотекой** - это полнофункциональное веб-приложение, разработанное с использованием Django Framework. Проект предоставляет комплексное решение для управления библиотечными операциями, включая управление книгами, студентами, авторами и выдачей книг.

**Library Management System** is a full-featured web application developed using Django Framework. The project provides a comprehensive solution for managing library operations, including books, students, authors and book issues management.

#### Ключевые возможности / Key Features

- **Реляционная база данных** с правильно настроенными связями между таблицами
- **Relational database** with properly configured table relationships
- **Интуитивная админ-панель** с выпадающими списками для удобного выбора связанных объектов
- **Intuitive admin panel** with dropdown lists for easy selection of related objects
- **CRUD операции** (создание, чтение, обновление, удаление) для всех сущностей
- **CRUD operations** (Create, Read, Update, Delete) for all entities
- **Система авторизации** для студентов и администраторов
- **Authentication system** for students and administrators
- **Автоматический расчет штрафов** за просроченные книги
- **Automatic fine calculation** for overdue books

### Структура базы данных / Database Structure

Приложение использует следующие взаимосвязанные модели:

#### 1. **Author** (Авторы)
- Имя автора
- Биография
- Связь: один автор → много книг

#### 2. **Category** (Категории)
- Название категории
- Описание
- Связь: одна категория → много книг

#### 3. **Book** (Книги)
- Название книги
- **ForeignKey** → Author (выбор из существующих авторов)
- ISBN
- **ForeignKey** → Category (выбор из существующих категорий)

#### 4. **Student** (Студенты)
- **OneToOneField** → User (связь с пользователем Django)
- Класс
- Филиал
- Номер студента
- Телефон
- Фото

#### 5. **IssuedBook** (Выданные книги)
- **ForeignKey** → Student (выбор студента из списка)
- **ForeignKey** → Book (выбор книги из списка)
- Дата выдачи
- Дата возврата
- Статус возврата

Developed web services using Python (Django Framework) where an admin can perform <code>C R U D</code> (Create, Read, Update and Delete) operations

### Установка и запуск / Installation and Setup

**Требования / Prerequisites:**

Backend: `Python 3.8+` & `Django 5.0+`
Frontend: `HTML` & `CSS`

**Шаги установки / Installation Steps:**

```bash
# 1. Клонируйте репозиторий / Clone the repository
git clone <repository-url>
cd Library_Management_System_Django

# 2. Установите зависимости / Install dependencies
pip install -r requirements.txt

# 3. Примените миграции / Apply migrations
python manage.py migrate

# 4. Создайте суперпользователя / Create a superuser
python manage.py createsuperuser

# 5. Запустите сервер / Run the development server
python manage.py runserver

# 6. (Опционально) Заполните базу тестовыми данными
# (Optional) Populate database with test data
python populate_db.py

# 7. Откройте в браузере / Open in browser
# Admin panel: http://127.0.0.1:8000/admin
# Main site: http://127.0.0.1:8000
```

### Как использовать выпадающие списки / How to use dropdown lists

При добавлении данных через админ-панель:

**When adding data via admin panel:**

1. **Добавление автора / Adding an author:**
   - Перейдите в раздел "Авторы" / Go to "Authors" section
   - Нажмите "Добавить автора" / Click "Add Author"
   - Заполните имя и биографию / Fill in name and biography

2. **Добавление категории / Adding a category:**
   - Перейдите в раздел "Категории" / Go to "Categories" section
   - Нажмите "Добавить категорию" / Click "Add Category"
   - Заполните название и описание / Fill in name and description

3. **Добавление книги / Adding a book:**
   - Перейдите в раздел "Книги" / Go to "Books" section
   - Нажмите "Добавить книгу" / Click "Add Book"
   - **Автор** выбирается из выпадающего списка существующих авторов
   - **Author** is selected from dropdown list of existing authors
   - **Категория** выбирается из выпадающего списка существующих категорий
   - **Category** is selected from dropdown list of existing categories

4. **Выдача книги студенту / Issuing a book to student:**
   - Перейдите в раздел "Выданные книги" / Go to "Issued Books" section
   - Нажмите "Добавить выданную книгу" / Click "Add Issued Book"
   - **Студент** выбирается из выпадающего списка
   - **Student** is selected from dropdown list
   - **Книга** выбирается из выпадающего списка
   - **Book** is selected from dropdown list

### Objective

**Anyone can**

1. see all the books in homepage

2. search books based on author or name of the book or category of the book

3. sort books or author alphabetically

**Student can**

1. login / signup ,

2. can request book

3. see their own issues and filter them based on :
   * requested issues ,
   * issued books or
   * all of them together
   
4. check their own fines

5. can see
   * the days remaining to return a particular book or
   * the number of days passed the return date of a particular book in the my fines page

**Admin can**

1. login to admin dashboard

2. check all issues :
   * see issues ,
   * delete issues ,
   * search issues by studentid
   * filter issues based on :
      * issued or not,
      * returned or not ,
      
3. accept a issue :
   * from the dashboard where admin has to manually select return date or
   * from the Issue requests page where return date is automatically calculated

4. add , delete search books and filter books based on author

5. add , delete , search author

6. calculate fine by clicking a button ,

7. create, delete fine ,search fines for studentid

8. toggle fine paid status (if paid in cash)

9. search ,modify,add,delete students , filter them based on department and check all fines and issues of that student

10. can see the last-login , date joined & the student associated to a particular user

11. can change password for any user

**More ...**

1. While signing up if studentID is already associated to a user in this platform then it will show a error without reloading the page and as soon as correct id is given then the error will go away

2. Books in homepage will show status of issued , issue requested or request issue based on whether the book is issued or requested for a issue or is not requested for logged-in students only


## Technologies used ⚙️

* <a href="https://github.com/mrankitgupta/Python-Roadmap">Python</a> <a href="https://github.com/mrankitgupta/Python-Roadmap" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="25" height="20"/> </a>

* <a href="https://github.com/mrankitgupta">Django</a> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://github.com/mrankitgupta/mrankitgupta/blob/main/images/icons8-django.svg" alt="django" width="40" height="30"/> </a>

* <a href="https://github.com/mrankitgupta">HTML</a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="30"/> </a>

* <a href="https://github.com/mrankitgupta">CSS</a> 

## For any queries/doubts 🔗 👇 

### [Ankit Gupta](https://bio.link/AnkitGupta)
<p align="left"> <a href="https://twitter.com/MrAnkitGupta_/" target="blank"><img src="https://img.shields.io/twitter/follow/MrAnkitGupta_?logo=twitter&style=for-the-badge" alt="MrAnkitGupta_" /></a> </p>

<a href="https://www.linkedin.com/in/mrankitgupta" target="blank"><img align="center" src="https://img.shields.io/badge/-MrAnkitGupta-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/mrankitgupta/" alt="MrAnkitGupta" height="20" width="100" /></a>
<a href="https://www.instagram.com/MrAnkitGupta_" target="blank"><img align="center" src="https://img.shields.io/badge/-@MrAnkitGupta_-D7008A?style=flat-square&labelColor=D7008A&logo=Instagram&logoColor=white&link=https://www.instagram.com/MrAnkitGupta_" alt="MrAnkitGupta_" height="20" width="110" /></a>
<a href="https://bio.link/AnkitGupta" target="blank"><img align="center" src="https://img.shields.io/badge/website-000000?style=for-the-badge&logo=About.me&logoColor=white&link=https://bio.link/AnkitGupta" alt="AnkitGupta" height="20" width="90" /></a>
<a href="https://github.com/mrankitgupta/" target="blank"><img align="center" src="https://img.shields.io/github/followers/mrankitgupta?label=Follow&style=social&link=https://github.com/mrankitgupta/" alt="MrAnkitGupta" height="20" width="90" /></a>

  
