from .serializers import CustomUserCreateSerializer
from Eventmain.ResponseFunction import *
from djoser.views import UserViewSet
from .models import *


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "create":  # Ensure custom serializer is used for registration
            return CustomUserCreateSerializer
        return super().get_serializer_class()
