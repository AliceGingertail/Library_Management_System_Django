# Generated migration for complete library system with all tables and ForeignKey relationships

import django.db.models.deletion
import library.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Имя автора"
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата рождения"
                    ),
                ),
                ("country", models.CharField(max_length=100, verbose_name="Страна")),
                ("bio", models.TextField(blank=True, verbose_name="Биография")),
            ],
            options={
                "verbose_name": "Автор",
                "verbose_name_plural": "Авторы",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Publisher",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название издательства"),
                ),
                ("address", models.TextField(verbose_name="Адрес")),
                ("contact", models.CharField(max_length=100, verbose_name="Контакт")),
            ],
            options={
                "verbose_name": "Издатель",
                "verbose_name_plural": "Издатели",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название категории"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="LibraryBranch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название филиала"),
                ),
                ("address", models.TextField(verbose_name="Адрес")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
            ],
            options={
                "verbose_name": "Филиал библиотеки",
                "verbose_name_plural": "Филиалы библиотеки",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("classroom", models.CharField(max_length=10, verbose_name="Класс")),
                (
                    "roll_no",
                    models.CharField(blank=True, max_length=3, verbose_name="Номер"),
                ),
                (
                    "phone",
                    models.CharField(blank=True, max_length=20, verbose_name="Телефон"),
                ),
                (
                    "image",
                    models.ImageField(blank=True, upload_to="students/", verbose_name="Фото"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="students",
                        to="library.librarybranch",
                        verbose_name="Филиал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Студент",
                "verbose_name_plural": "Студенты",
                "ordering": ["user__username"],
            },
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee_id",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="ID сотрудника"
                    ),
                ),
                ("position", models.CharField(max_length=100, verbose_name="Должность")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="staff",
                        to="library.librarybranch",
                        verbose_name="Филиал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сотрудник",
                "verbose_name_plural": "Сотрудники",
                "ordering": ["employee_id"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Название книги")),
                ("isbn", models.PositiveIntegerField(verbose_name="ISBN")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="library.author",
                        verbose_name="Автор",
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="library.publisher",
                        verbose_name="Издатель",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="library.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="library.librarybranch",
                        verbose_name="Филиал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Книга",
                "verbose_name_plural": "Книги",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="IssuedBook",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "issued_date",
                    models.DateField(auto_now=True, verbose_name="Дата выдачи"),
                ),
                (
                    "expiry_date",
                    models.DateField(
                        default=library.models.expiry, verbose_name="Дата возврата"
                    ),
                ),
                ("returned", models.BooleanField(default=False, verbose_name="Возвращена")),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issued_books",
                        to="library.student",
                        verbose_name="Студент",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issues",
                        to="library.book",
                        verbose_name="Книга",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="issued_books",
                        to="library.staff",
                        verbose_name="Сотрудник",
                    ),
                ),
            ],
            options={
                "verbose_name": "Выданная книга",
                "verbose_name_plural": "Выданные книги",
                "ordering": ["-issued_date"],
            },
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "reservation_date",
                    models.DateField(auto_now_add=True, verbose_name="Дата резервирования"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает"),
                            ("fulfilled", "Выполнено"),
                            ("cancelled", "Отменено"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "expiry_date",
                    models.DateField(
                        default=library.models.expiry, verbose_name="Срок действия"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="library.student",
                        verbose_name="Студент",
                    ),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="library.book",
                        verbose_name="Книга",
                    ),
                ),
            ],
            options={
                "verbose_name": "Резервирование",
                "verbose_name_plural": "Резервирования",
                "ordering": ["-reservation_date"],
            },
        ),
        migrations.CreateModel(
            name="Fines",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Сумма"
                    ),
                ),
                ("reason", models.TextField(verbose_name="Причина")),
                ("paid", models.BooleanField(default=False, verbose_name="Оплачено")),
                (
                    "created_date",
                    models.DateField(auto_now_add=True, verbose_name="Дата создания"),
                ),
                (
                    "issued_book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fines",
                        to="library.issuedbook",
                        verbose_name="Выданная книга",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fines",
                        to="library.student",
                        verbose_name="Студент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Штраф",
                "verbose_name_plural": "Штрафы",
                "ordering": ["-created_date"],
            },
        ),
    ]
