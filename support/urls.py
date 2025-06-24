from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FAQViewSet,
    SupportRequestViewSet,
    ContactInfoViewSet,
)

router = DefaultRouter()

router.register(r"faqs", FAQViewSet, basename="faq")
router.register(r"support-requests", SupportRequestViewSet, basename="support_request")
router.register(r"contact-info", ContactInfoViewSet, basename="contact_info")

urlpatterns = [
    path("support/", include(router.urls)),
]
