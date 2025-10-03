from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


class DeleteUserSignalsTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.u2 = User.objects.create_user(username='u2', email='u2@example.com', password='pass')
        # create message and related data
        self.msg = Message.objects.create(sender=self.u1, receiver=self.u2, content='Hello')
        # create a history entry by editing
        self.msg.content = 'Edited'
        self.msg._editor = self.u1
        self.msg.save()

    def test_delete_user_cleans_related(self):
        # delete u1 and ensure data related to u1 is cleaned
        uid = self.u1.pk
        self.u1.delete()
        # Messages where u1 was sender should be deleted
        self.assertFalse(Message.objects.filter(sender__pk=uid).exists())
        # Notifications for u1 should be deleted
        self.assertFalse(Notification.objects.filter(user__pk=uid).exists())
        # MessageHistory entries where editor was u1 should be deleted
        self.assertFalse(MessageHistory.objects.filter(editor__pk=uid).exists())
