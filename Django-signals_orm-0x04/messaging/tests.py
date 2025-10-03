from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification
from .models import MessageHistory


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

    def test_message_history_on_edit(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content='First')
        # Edit the message
        msg.content = 'Edited'
        # simulate view attaching the editor
        msg._editor = self.u1
        msg.save()

        # There should be a history entry
        hist = MessageHistory.objects.filter(message=msg)
        # Because we created the history using prev instance, history.message points to the same message
        self.assertEqual(hist.count(), 1)
        h = hist.first()
        self.assertEqual(h.old_content, 'First')
        # The message should be marked as edited
        msg.refresh_from_db()
        self.assertTrue(msg.edited)
        # the edited_by field should point to the editor
        self.assertEqual(msg.edited_by, self.u1)
        # history editor recorded
        self.assertEqual(h.editor, self.u1)
