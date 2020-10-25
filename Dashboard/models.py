from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return self.name

class People(models.Model):
    pass

class Class(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    student = models.ManyToManyField(People, related_name="classes")
    teaching_assistant = models.ManyToManyField(People, related_name="assist_classes")
    def __str__(self):
        return f"{self.name} by {self.instructor}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="notifications_sent")
    class_group = models.ForeignKey(Class, on_delete=models.PROTECT, related_name="notifications")
    topic = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reciepent = models.CharField(max_length=255)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.name,
            "recipient": [user.email for user in self.recipients.all()],
            "topic": self.topic,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M: %S"),
        }

    

