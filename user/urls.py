from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *



urlpatterns = [
    path('auth/users/', CustomUserViewSet.as_view({'post': 'create'}), name='register'),
]