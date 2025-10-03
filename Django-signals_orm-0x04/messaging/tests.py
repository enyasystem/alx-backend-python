from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification


User = get_user_model()


class MessagingSignalsTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.u2 = User.objects.create_user(username='u2', email='u2@example.com', password='pass')

    def test_notification_created_on_message(self):
        # create a message from u1 to u2
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content='Hello')
        # notification should be created for u2
        nots = Notification.objects.filter(user=self.u2, message=msg)
        self.assertEqual(nots.count(), 1)
        notif = nots.first()
        self.assertFalse(notif.read)
        self.assertEqual(notif.message, msg)
