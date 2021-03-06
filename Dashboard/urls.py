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
    path("logout_student", views.logout_student, name="logout_student"),
    path("add_token", views.add_token),
    path("add_class", views.add_class, name="add_class"),
    path("<int:id>/class_view", views.class_view, name="class_view"),
    path("<int:id>/add_student", views.add_student, name="add_student"),
    path("<int:id>/add_ta", views.add_ta, name="add_ta"),
    path("<int:id>/notification_view", views.notification_view, name="notification_view"),
    path("get_classes", views.get_classes),
    path("seen_notif", views.seen_notif),
    path("<int:id>/remove_student", views.remove_student, name="remove_student"),
    path("get_notifications", views.get_notifications),

]
