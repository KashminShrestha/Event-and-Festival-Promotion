# admin.py
from django.contrib import admin
from .models import FCMTokens, NotificationToken

@admin.register(FCMTokens)
class FCMTokensAdmin(admin.ModelAdmin):
    list_display = ('id', 'fcm_token')
    search_fields = ('fcm_token',)

@admin.register(NotificationToken)
class NotificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'token')
    search_fields = ('token', 'owner__email')  # Adjust based on your User model
    autocomplete_fields = ['owner']
