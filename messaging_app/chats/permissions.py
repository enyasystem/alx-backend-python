from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """Allow access only to conversation participants."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if hasattr(obj, 'participants'):
            return obj.participants.filter(pk=user.pk).exists()

        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False


class IsSenderOrParticipant(permissions.BasePermission):
    """Allow message creation if the request.user is a participant in the conversation or the sender."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method == 'POST':
            conversation_id = request.data.get('conversation')
            if not conversation_id:
                return False
            from .models import Conversation

            try:
                conv = Conversation.objects.get(conversation_id=conversation_id)
            except Conversation.DoesNotExist:
                return False

            return conv.participants.filter(pk=user.pk).exists()

        return True


class IsParticipantOfConversation(permissions.BasePermission):
    """Combined permission:

    - Allow only authenticated users.
    - Allow only participants of a conversation to view/update/delete messages or the conversation.
    - Allow creation of messages only if the requesting user is a participant of the referenced conversation.
    - Allow creation of conversations for authenticated users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # If creating a message, ensure the user is a participant of the conversation
        if request.method == 'POST' and getattr(view, 'basename', '') in ('conversation-messages', 'message'):
            conversation_id = request.data.get('conversation')
            if not conversation_id:
                return False
            from .models import Conversation
            try:
                conv = Conversation.objects.get(conversation_id=conversation_id)
            except Conversation.DoesNotExist:
                return False
            return conv.participants.filter(pk=user.pk).exists()

        # For creating conversations, any authenticated user may create
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Conversation instance
        if hasattr(obj, 'participants'):
            return obj.participants.filter(pk=user.pk).exists()

        # Message instance
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False
