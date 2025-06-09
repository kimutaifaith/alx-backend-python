from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only if the message already exists (not a new message)
        old_message = Message.objects.get(pk=instance.pk)
        if instance.content != old_message.content:
            # Store old content in MessageHistory
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=instance.edited_by  # Assuming edited_by is set before save
            )
            instance.edited = True

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()