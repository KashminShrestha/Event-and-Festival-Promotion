import firebase_admin
from firebase_admin import credentials, messaging
import os

from django.conf import settings


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
