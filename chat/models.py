from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    playerA = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='chatroomsA')
    playerB = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='chatroomsB')
    createAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playerA', 'playerB')

    def __str__(self):
        return f"Chat between {self.playerA.username} and {self.playerB.username}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    createAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['createAt']

    def __str__(self):
        return f"{self.room} - {self.sender.username}: {self.content[:20]}"

class MessageDeletion(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    deleted = models.DateTimeField()
    
    class Meta:
        unique_together = ('room', 'player')

    def __str__(self):
        return f"{self.room} - {self.player} deleted from {self.deleted}"
