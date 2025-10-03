from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class UnreadManagerTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', email='u1@example.com', password='pass')
        self.u2 = User.objects.create_user(username='u2', email='u2@example.com', password='pass')
        Message.objects.create(sender=self.u1, receiver=self.u2, content='One', read=False)
        Message.objects.create(sender=self.u1, receiver=self.u2, content='Two', read=True)

    def test_unread_manager_returns_only_unread(self):
        qs = Message.unread.unread_for(self.u2)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.only('content').first().content, 'One')