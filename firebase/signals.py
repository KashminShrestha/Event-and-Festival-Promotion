from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from Eventmain.models import Event
from firebase.models import NotificationToken
from firebase.utils import create_and_send_notification

@receiver(pre_save, sender=Event)
def store_old_status(sender, instance, **kwargs):
    """
    Store the old status of the event before saving.
    This is used to determine if the status has changed.
    """
    if instance.pk:
        try:
            instance._old_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Event)
def notify_users_on_publish(sender, instance, created, **kwargs):
    """
    Send notifications to all users when an event is published.
    
    When an event status changes to 'published', this signal:
    1. Creates a notification record for each user with a token
    2. Sends a push notification to those users
    
    Args:
        sender: The model class (Event)
        instance: The actual event instance that was saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional arguments
    """
    # On creation and status is published
    if created and instance.status == 'published':
        tokens = NotificationToken.objects.all()
        for token_obj in tokens:
            if token_obj.owner:
                create_and_send_notification(
                    user=token_obj.owner,
                    event=instance,
                    message=instance.description[:100] + "...",
                    medium='push',
                    title=f"New Event: {instance.name}"
                )
    # On update and status changed to published
    elif not created:
        old_status = getattr(instance, '_old_status', None)
        if old_status != 'published' and instance.status == 'published':
            tokens = NotificationToken.objects.all()
            for token_obj in tokens:
                if token_obj.owner:
                    create_and_send_notification(
                        user=token_obj.owner,
                        event=instance,
                        message=instance.description[:100] + "...",
                        medium='push',
                        title=f"New Event: {instance.name}"
                    )

