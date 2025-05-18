from django.db import models
from  Eventmain.models import Notification
# Create your models here.
from django.db import models

from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class FCMTokens(models.Model):
   fcm_token = models.CharField(max_length=255)

   def __str__(self):
      return self.fcm_token

class NotificationToken(models.Model):
   owner = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
   token = models.CharField(max_length=255, unique=True)
   
   def __str__(self):
      return self.token