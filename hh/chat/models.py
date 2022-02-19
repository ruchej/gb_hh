from django.contrib.auth import get_user_model
from django.db import models

from resumes.models import Resume
from recruiting.models import Response

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    resume = models.ForeignKey(Resume, blank=True, null=True, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return " - ".join([cont.user.username for cont in self.participants.all()])
