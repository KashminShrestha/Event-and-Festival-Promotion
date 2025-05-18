from rest_framework import serializers
from .models import *

class NotificationTokenSerializer(serializers.ModelSerializer):
   class Meta:
      model = NotificationToken
      fields = '__all__'