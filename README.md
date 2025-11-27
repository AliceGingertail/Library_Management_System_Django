# Library Management System using Python on Django Framework

## Установка и запуск на Arch Linux

### Предварительные требования

Убедитесь, что в вашей системе установлены следующие пакеты:

```bash
sudo pacman -S python python-pip git
```

### Установка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/AliceGingertail/Library_Management_System_Django.git
cd Library_Management_System_Django
```

2. **Создайте виртуальное окружение (рекомендуется):**

```bash
python -m venv venv
source venv/bin/activate
```

3. **Установите Django:**

```bash
pip install django
```

### Запуск проекта

1. **Примените миграции базы данных:**

```bash
python manage.py migrate
```

2. **Создайте суперпользователя (администратора):**

```bash
python manage.py createsuperuser
```

Следуйте инструкциям на экране для создания учетной записи администратора.

3. **Запустите сервер разработки:**

```bash
python manage.py runserver
```

4. **Откройте браузер и перейдите по адресу:**

- Главная страница: http://127.0.0.1:8000/
- Админ панель: http://127.0.0.1:8000/admin/

### Дополнительные команды

**Создание статических файлов (если необходимо):**
```bash
python manage.py collectstatic
```

**Запуск на другом порту:**
```bash
python manage.py runserver 8080
```

**Запуск с доступом из внешней сети:**
```bash
python manage.py runserver 0.0.0.0:8000
```

### Деактивация виртуального окружения

```bash
deactivate
```

### Структура проекта

```
Library_Management_System_Django/
├── LibraryManagementSystem/  # Основные настройки проекта
│   ├── settings.py           # Конфигурация Django
│   ├── urls.py               # Главный роутинг
│   └── wsgi.py               # WSGI конфигурация
├── library/                  # Основное приложение
│   ├── models.py             # Модели данных
│   ├── views.py              # Представления
│   ├── forms.py              # Формы
│   ├── templates/            # HTML шаблоны
│   └── static/               # Статические файлы (CSS, JS)
├── db.sqlite3                # База данных SQLite
└── manage.py                 # Скрипт управления Django
```

### Устранение неполадок

**Ошибка "No module named 'django'":**
```bash
pip install django
```

**Ошибка с правами доступа:**
```bash
chmod +x manage.py
```

**Проблемы с базой данных:**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---
