from django.db import models
from django.contrib.auth.models import User

from item.models import Items
# Create your models here.

class Conversation(models.Model):
    item = models.ForeignKey(Items, related_name='conversation', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversation')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =('-modified_at',)
        db_table = 'conversation'

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='message', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_message', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ConversationMessage'