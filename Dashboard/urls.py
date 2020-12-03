from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_notification", views.notification, name="notification"),
    path("pending_instructor", views.pending_instructor, name="pending_instructor"),
    path("<int:id>/add_instructor", views.add_instructor, name="add_instructor"),
    path("<int:id>/delete_instructor", views.delete_instructor, name="delete_instructor"),
    path("register_student", views.register_student, name="register_student"),
    path("login_student", views.login_student, name="login_student"),
]
