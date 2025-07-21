from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
class User(AbstractUser):
  user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=15, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username','first_name', 'last_name','password']

  def __str__(self):
    return self.email

  
class Conversation(models.Model):
  conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  participants = models.ManyToManyField('User',related_name='conversations')
  created_at =models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"Conversation {self.conversation_id}"

class Message(models.Model):
  message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
  sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
  message_body = models.TextField()
  sent_at = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)

  def __str__(self):
    return f"Message from {self.sender.username} in Conversation {self.conversation.conversation_id}"

  
  
   

