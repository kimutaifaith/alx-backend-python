from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username='alice', password='pass123')
        receiver = User.objects.create_user(username='bob', password='pass123')
        
        message = Message.objects.create(sender=sender, receiver=receiver, content='Hello Bob!')

        notification = Notification.objects.get(user=receiver, message=message)
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.user.username, 'bob')
