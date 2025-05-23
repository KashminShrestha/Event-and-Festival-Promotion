import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings
from django.core.mail import send_mail
from Eventmain.models import Notification
from .models import NotificationToken
import logging

logger = logging.getLogger(__name__)
# Check if Firebase is already initialized
if not firebase_admin._apps:
    cred_path = os.path.join(settings.BASE_DIR, 'firebase_key.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


def send_fcm_notification(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=token
        )
        response = messaging.send(message)
        return response
    except Exception as e:
        return str(e)

logger = logging.getLogger(__name__)

def create_and_send_notification(user, event, message, medium='push', **kwargs):
    """
    Create notification record and send it through the appropriate channel.
    
    This function serves as the central hub for all notification activities:
    1. Creates a record in the Notification database table
    2. Attempts to send the notification via the specified medium
    3. Updates the notification status based on delivery success/failure
    
    Args:
        user (User): The recipient user object
        event (Event): The related event object
        message (str): The notification message content
        medium (str): Delivery channel - 'push', 'email', or 'sms'
        **kwargs: Additional parameters for specific notification types
            - title (str): Optional notification title (defaults to event name)
            - icon (str): Optional icon URL for push notifications
    
    Returns:
        Notification: The created notification object with updated status
    
    Example:
        >>> user = User.objects.get(id=1)
        >>> event = Event.objects.get(id=5)
        >>> notify = create_and_send_notification(
        ...     user, 
        ...     event, 
        ...     "Your booking is confirmed!", 
        ...     medium='email'
        ... )
    """
    # Extract additional parameters
    title = kwargs.get('title', f"Event: {event.name}")
    
    # Create notification record with pending status
    notification = Notification.objects.create(
        user=user,
        event=event,
        message=message,
        medium=medium,
        status='pending'
    )
    
    # Send via appropriate channel
    try:
        if medium == 'push':
            # Get user's token
            token_obj = NotificationToken.objects.filter(owner=user).first()
            if token_obj:
                response = send_fcm_notification(
                    token=token_obj.token,
                    title=title,
                    body=message
                )
                notification.status = 'sent'
                logger.info(f"Push notification sent to user {user.id}: {response}")
            else:
                notification.status = 'failed'
                logger.warning(f"Push notification failed: No token for user {user.id}")
        
        elif medium == 'email':
            # You'll implement this function next
            send_email_notification(user, message, event, title)
            notification.status = 'sent'
            logger.info(f"Email notification sent to user {user.id}")
        
        elif medium == 'sms':
            # You'll implement this function next
            send_sms_notification(user, message, event)
            notification.status = 'sent'
            logger.info(f"SMS notification sent to user {user.id}")
        
        else:
            notification.status = 'failed'
            logger.error(f"Invalid notification medium: {medium}")
    
    except Exception as e:
        notification.status = 'failed'
        logger.exception(f"Failed to send {medium} notification: {str(e)}")
    
    # Save the updated status
    notification.save()
    return notification


def send_email_notification(user, message, event, subject=None):
    """
    Send an email notification to a user.
    
    Args:
        user (User): The recipient user object
        message (str): The email message body
        event (Event): The related event object
        subject (str, optional): Custom email subject. Defaults to event name.
    
    Returns:
        bool: True if sent successfully, False otherwise
    
    Example:
        >>> send_email_notification(
        ...     user, 
        ...     "Your ticket is confirmed!", 
        ...     event,
        ...     "Booking Confirmation"
        ... )
    """
    
    # Use provided subject or default to event name
    email_subject = subject or f"Event Notification: {event.name}"
    
    try:
        send_mail(
            subject=email_subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.exception(f"Email sending failed: {str(e)}")
        return False
    
def send_sms_notification(user, message, event):
    """
    Send an SMS notification to a user.
    
    This function provides a template for SMS integration.
    Note: Actual implementation requires a third-party SMS service.
    
    Args:
        user (User): The recipient user object
        message (str): The SMS message content
        event (Event): The related event object
    
    Returns:
        bool: True if sent successfully, False otherwise
        
    Example:
        >>> send_sms_notification(
        ...     user, 
        ...     "Your booking for Dashain Festival is confirmed!", 
        ...     event
        ... )
    """
    # This is a placeholder. You'll need to integrate with an SMS service
    # like Twilio, Sparrow SMS, or another Nepal-compatible SMS gateway
    
    # For now, we'll log the intent and return success
    # When integrating a real SMS service, replace this with actual API calls
    
    logger.info(f"SMS would be sent to {user.id} about event {event.id}: {message}")
    
    # this commented code adapts this code when integrating a real SMS service
    """
    # Example using Twilio
    from twilio.rest import Client
    
    # Get credentials from settings
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_PHONE_NUMBER
    
    # Get user's phone number (adjust field name as needed)
    to_number = user.phone_number
    
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    
    # Send message
    try:
        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        return True
    except Exception as e:
        logger.exception(f"SMS sending failed: {str(e)}")
        return False
    """
    
    return True  # Placeholder return value

