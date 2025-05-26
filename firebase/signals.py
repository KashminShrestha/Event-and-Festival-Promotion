from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from Eventmain.models import Event, Booking  # Add Booking import
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

# ===== BOOKING NOTIFICATION SIGNALS =====

@receiver(pre_save, sender=Booking)
def store_old_booking_status(sender, instance, **kwargs):
    """
    Store the old status of the booking before saving.
    This is used to determine if the booking status has changed.
    """
    if instance.pk:
        try:
            instance._old_booking_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._old_booking_status = None
    else:
        instance._old_booking_status = None

@receiver(post_save, sender=Booking)
def notify_user_on_booking_change(sender, instance, created, **kwargs):
    """
    Send notifications to the user when a booking is created or status changes.
    
    Sends notifications for:
    - Booking confirmation (when status becomes 'paid')
    - Booking cancellation (when status becomes 'cancelled') 
    - Booking refund (when status becomes 'refunded')
    """
    user = instance.user
    event = instance.ticket.event
    
    # Booking Confirmation (when payment is verified)
    if not created:  # Only on updates
        old_status = getattr(instance, '_old_booking_status', None)
        
        if old_status != 'paid' and instance.status == 'paid':
            # Payment just got verified - send confirmation
            message = f"Your booking for {event.name} is confirmed! Quantity: {instance.quantity}, Total: Rs. {instance.total_amount}. Your QR code ticket has been generated."
            
            # Send Email (required by requirements)
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='email',
                title=f"Booking Confirmed - {event.name}"
            )
            
            # Send Push notification
            create_and_send_notification(
                user=user, 
                event=event, 
                message=f"Booking confirmed for {event.name}!", 
                medium='push',
                title="Booking Confirmed"
            )
            
            # Send SMS (required by requirements)
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='sms'
            )
        
        # Booking Cancellation
        elif old_status != 'cancelled' and instance.status == 'cancelled':
            message = f"Your booking for {event.name} has been cancelled."
            
            # Send Email
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='email',
                title=f"Booking Cancelled - {event.name}"
            )
            
            # Send Push
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='push',
                title="Booking Cancelled"
            )
            
            # Send SMS
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='sms'
            )
        
        # Booking Refund
        elif old_status != 'refunded' and instance.status == 'refunded':
            message = f"Your booking for {event.name} has been refunded. Amount: Rs. {instance.total_amount}."
            
            # Send Email
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='email',
                title=f"Booking Refunded - {event.name}"
            )
            
            # Send Push
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='push',
                title="Booking Refunded"
            )
            
            # Send SMS
            create_and_send_notification(
                user=user, 
                event=event, 
                message=message, 
                medium='sms'
            )
