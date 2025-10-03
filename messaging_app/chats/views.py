

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsSenderOrParticipant

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']
    permission_classes = [IsAuthenticated, IsParticipant]

    def get_queryset(self):
        # Return only conversations where the requesting user is a participant
        user = self.request.user
        return Conversation.objects.filter(participants__pk=user.pk).distinct()

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        conversation = Conversation.objects.create()
        if participants_ids:
            users = User.objects.filter(user_id__in=participants_ids)
            conversation.participants.set(users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__conversation_id', 'sender__username']
    permission_classes = [IsAuthenticated, IsParticipant, IsSenderOrParticipant]

    def get_queryset(self):
        # Messages from conversations where the user participates
        user = self.request.user
        return Message.objects.filter(conversation__participants__pk=user.pk).distinct()

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'Invalid conversation or sender.'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(conversation=conversation, sender=sender, message_body=message_body)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
