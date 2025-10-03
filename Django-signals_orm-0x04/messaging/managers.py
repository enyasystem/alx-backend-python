from django.db import models


class UnreadMessagesManager(models.Manager):
    """Manager to return unread messages for a given user, optimized for inbox listing."""
    def unread_for_user(self, user):
        # Use select_related to bring sender in a single query and only select required fields
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .select_related('sender')
            .only('message_id', 'sender__username', 'content', 'sent_at')
        )

    # Backwards-compatible alias used in older tests/code
    def unread_for(self, user):
        return self.unread_for_user(user)
