from django.db.models.signals import post_save
from django.dispatch import receiver
from Eventmain.models import Event
from firebase.models import NotificationToken
from firebase.utils import send_fcm_notification

@receiver(post_save, sender=Event)
def notify_users_on_publish(sender, instance, created, **kwargs):
    if instance.status == 'published':
        tokens = NotificationToken.objects.all().values_list('token', flat=True)
        for token in tokens:
            send_fcm_notification(
                token=token,
                title=f"New Event: {instance.name}",
                body=instance.description[:100]
            )
