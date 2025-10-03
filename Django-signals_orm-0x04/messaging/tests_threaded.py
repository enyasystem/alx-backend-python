from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from .models import Message
from .views import threaded_message
import json


User = get_user_model()


class ThreadedViewQueryCountTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', 'u1@example.com', 'pass')
        self.u2 = User.objects.create_user('u2', 'u2@example.com', 'pass')
        # root
        self.root = Message.objects.create(sender=self.u1, receiver=self.u2, content='root')
        # two children
        c1 = Message.objects.create(sender=self.u1, receiver=self.u2, content='c1', parent_message=self.root)
        c2 = Message.objects.create(sender=self.u1, receiver=self.u2, content='c2', parent_message=self.root)
        # grandchildren
        Message.objects.create(sender=self.u1, receiver=self.u2, content='c1-1', parent_message=c1)
        Message.objects.create(sender=self.u1, receiver=self.u2, content='c1-2', parent_message=c1)
        Message.objects.create(sender=self.u1, receiver=self.u2, content='c2-1', parent_message=c2)

    def test_threaded_view_query_count(self):
        factory = RequestFactory()
        request = factory.get('/')
        request.user = self.u2

        # Manager uses select_related and prefetch_related; keep queries small.
        # Allow up to 6 queries to be conservative (root fetch + prefetch queries).
        with self.assertNumQueries(6):
            resp = threaded_message(request, str(self.root.message_id))

        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('thread', data)
        self.assertEqual(data['thread']['message_id'], str(self.root.message_id))
        # should have at least two direct replies
        self.assertTrue(len(data['thread']['replies']) >= 2)
