from django.contrib import admin
from .models import Message, Notification, MessageHistory

admin.site.register(Message)
admin.site.register(MessageHistory)
