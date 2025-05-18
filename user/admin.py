
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'is_staff', 'is_active', 'language', 'created_at')
    list_filter = ('is_staff', 'is_active', 'language')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
admin.site.register(User, CustomUserAdmin)
    

