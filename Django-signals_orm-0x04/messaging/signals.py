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
