from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"ChatRoom {self.id}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.sender} in {self.room}: {self.message[:20]}" 