from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """When a Message is created, make a Notification for the receiver."""
    if not created:
        return

    Notification.objects.create(user=instance.receiver, message=instance)


from django.db.models.signals import pre_save


@receiver(pre_save, sender=Message)
def record_message_history(sender, instance, **kwargs):
    """Before a Message is updated, save the old content into MessageHistory."""
    # If instance is new (no PK), nothing to record
    if not instance.pk:
        return

    try:
        prev = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content changed, create history record and set edited flag
    if prev.content != instance.content:
        from .models import MessageHistory
        # Check for an attached editor on the instance (set by view or save caller)
        editor = getattr(instance, '_editor', None)
        MessageHistory.objects.create(message=prev, old_content=prev.content, editor=editor)
        instance.edited = True
        if editor:
            instance.edited_by = editor


    # Cleanup related data when a user is deleted
    from django.db.models.signals import post_delete
    from django.contrib.auth import get_user_model
    from django.db import models as dj_models


    @receiver(post_delete, sender=get_user_model())
    def cleanup_user_related(sender, instance, **kwargs):
        """Ensure messages, notifications and histories related to the deleted user are removed."""
        from .models import MessageHistory
        # Delete MessageHistory entries where editor was the user
        MessageHistory.objects.filter(editor=instance).delete()

        # Delete Notifications for the user
        Notification.objects.filter(user=instance).delete()

        # Delete any messages where the user was sender or receiver
        Message.objects.filter(dj_models.Q(sender=instance) | dj_models.Q(receiver=instance)).delete()
