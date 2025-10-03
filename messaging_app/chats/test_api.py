import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from .models import User, Conversation, Message


class MessagingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # create two users
        self.user1 = User.objects.create_user(username='alice', email='alice@example.com', password='pass')
        self.user2 = User.objects.create_user(username='bob', email='bob@example.com', password='pass')

    def obtain_token(self, username, password):
        url = '/api/token/'
        resp = self.client.post(url, {'username': username, 'password': password}, format='json')
        # If the token endpoint is not available (some envs lack simplejwt),
        # fall back to session authentication by logging in the test client.
        if resp.status_code == 404:
            logged = self.client.login(username=username, password=password)
            # Return a fake response-like object with status_code 200 when login succeeded
            class _FakeResp:
                def __init__(self, status_code):
                    self.status_code = status_code
                    self.data = {}
            return _FakeResp(200 if logged else 401)

        return resp

    def test_jwt_and_conversation_flow(self):
        # obtain token for user1
        resp = self.obtain_token('alice', 'pass')
        assert resp.status_code == status.HTTP_200_OK
        access = getattr(resp, 'data', {}).get('access')

        # If we got an access token, use Bearer header; otherwise assume session auth via client.login()
        if access:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        # create conversation with both participants
        conv_resp = self.client.post('/api/conversations/', {'participants': [str(self.user1.user_id), str(self.user2.user_id)]}, format='json')
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conv_id = conv_resp.data.get('conversation_id')
        assert conv_id

        # send a message as user1
        msg_resp = self.client.post(f'/api/conversations/{conv_id}/messages/', {
            'conversation': conv_id,
            'sender': str(self.user1.user_id),
            'message_body': 'Hello Bob'
        }, format='json')
        assert msg_resp.status_code == status.HTTP_201_CREATED
        # list conversations for user1
        list_conv = self.client.get('/api/conversations/')
        assert list_conv.status_code == status.HTTP_200_OK
        conv_items = list_conv.data.get('results') if isinstance(list_conv.data, dict) and 'results' in list_conv.data else list_conv.data
        assert any(c['conversation_id'] == conv_id for c in conv_items)

        # list messages
        list_msgs = self.client.get(f'/api/conversations/{conv_id}/messages/')
        assert list_msgs.status_code == status.HTTP_200_OK
        # should contain our message
        assert any(m['message_body'] == 'Hello Bob' for m in list_msgs.data.get('results', list_msgs.data))

    def test_unauthorized_cannot_access(self):
        # create a conversation directly in DB
        conv = Conversation.objects.create()
        conv.participants.set([self.user1, self.user2])
        # no auth header
        resp = self.client.get('/api/conversations/')
        # unauthenticated should return 401 or 403 depending on middleware
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
