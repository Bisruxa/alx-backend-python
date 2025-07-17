from django.db import models
from django.contrib.auth.models import AbstractUser,
class User(AbstractUser):
  email = models.EmailField(unique=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.email

  
class conversation(models.Model):
  participants = models.ManyToMany('User',related_name='conversations')
  created_at =models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return f"Conversation {self.id}"
class message(models.Model):
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
  sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)

  def __str__(self):
    return f"Message from {self.sender.username} in Conversation {self.conversation.id}"
  
  
   

