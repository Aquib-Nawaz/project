from django.contrib import admin
from .models import User, Notification, Classes

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Classes)
# Register your models here.
