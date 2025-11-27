from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_book/", views.add_book, name="add_book"),
    path("view_books/", views.view_books, name="view_books"),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
    path("delete_issue/<int:myid>/", views.delete_issue, name="delete_issue"),

    # Author URLs
    path("add_author/", views.add_author, name="add_author"),
    path("view_authors/", views.view_authors, name="view_authors"),
    path("delete_author/<int:myid>/", views.delete_author, name="delete_author"),

    # Publisher URLs
    path("add_publisher/", views.add_publisher, name="add_publisher"),
    path("view_publishers/", views.view_publishers, name="view_publishers"),
    path("delete_publisher/<int:myid>/", views.delete_publisher, name="delete_publisher"),

    # Category URLs
    path("add_category/", views.add_category, name="add_category"),
    path("view_categories/", views.view_categories, name="view_categories"),
    path("delete_category/<int:myid>/", views.delete_category, name="delete_category"),

    # LibraryBranch URLs
    path("add_branch/", views.add_branch, name="add_branch"),
    path("view_branches/", views.view_branches, name="view_branches"),
    path("delete_branch/<int:myid>/", views.delete_branch, name="delete_branch"),

    # Staff URLs
    path("add_staff/", views.add_staff, name="add_staff"),
    path("view_staff/", views.view_staff, name="view_staff"),
    path("delete_staff/<int:myid>/", views.delete_staff, name="delete_staff"),

    # Reservation URLs
    path("add_reservation/", views.add_reservation, name="add_reservation"),
    path("view_reservations/", views.view_reservations, name="view_reservations"),
    path("delete_reservation/<int:myid>/", views.delete_reservation, name="delete_reservation"),

    # Fines URLs
    path("add_fine/", views.add_fine, name="add_fine"),
    path("view_fines/", views.view_fines, name="view_fines"),
    path("delete_fine/<int:myid>/", views.delete_fine, name="delete_fine"),
    path("mark_fine_paid/<int:myid>/", views.mark_fine_paid, name="mark_fine_paid"),
]