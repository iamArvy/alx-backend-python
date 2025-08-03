from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:  # Content changed
                MessageHistory.objects.create(
                    message=instance,
                    content=original.content,
                    edited_by=instance.edited_by if hasattr(instance, 'edited_by') else None
                )
                instance.edited = True
                instance.last_edited = timezone.now()
        except Message.DoesNotExist:
            pass



@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Explicitly clean up related data that wouldn't be caught by CASCADE
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).update(edited_by=None)