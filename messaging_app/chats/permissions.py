from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """Allow access only to conversation participants."""

    def has_object_permission(self, request, view, obj):
        # obj can be Conversation or Message
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # If obj is a Conversation instance
        if hasattr(obj, 'participants'):
            return obj.participants.filter(pk=user.pk).exists()

        # If obj is a Message instance, check message.conversation participants
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False


class IsSenderOrParticipant(permissions.BasePermission):
    """Allow message creation if the request.user is a participant in the conversation or the sender."""

    def has_permission(self, request, view):
        # For list/create actions, ensure user is participant of conversation (if provided)
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # For create, conversation id will be in request.data
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

        # For other safe methods, allow and defer to object permission
        return True
