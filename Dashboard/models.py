from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    role = models.CharField(max_length=255, default="NONE")
    token = models.CharField(max_length=255, null=True)

class Classes(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teach_classes")
    students = models.ManyToManyField(User, related_name="in_classes")
    teaching_assistant = models.ManyToManyField(User, related_name="assist_classes")
    def __str__(self):
        return f"{self.name} by {self.instructor}"
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            #"recipient": [user.email for user in self.recipients.all()],
        }

class Notification(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_namcle="notifications")
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="notifications_sent")
    class_group = models.ForeignKey(Classes, on_delete=models.PROTECT, related_name="class_notification")
    topic = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.ManyToManyField(User, related_name="recieved_notif")
    reciepent = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.name,
            #"recipient": [user.email for user in self.recipients.all()],
            "topic": self.topic,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M: %S"),
        }

    

