from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import FAQ, SupportRequest, ContactInfo
from .serializers import FAQSerializer, SupportRequestSerializer, ContactInfoSerializer
from rest_framework.exceptions import PermissionDenied


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    "message": "FAQ created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Failed to create FAQ.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    "message": "FAQ updated successfully.",
                    "data": serializer.data,
                }
            )
        return Response(
            {"message": "Failed to update FAQ.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "FAQ deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class SupportRequestViewSet(viewsets.ModelViewSet):
    serializer_class = SupportRequestSerializer

    def get_permissions(self):
        permission_map = {
            "create": [IsAuthenticated],
            "list": [IsAdminUser],
            "retrieve": [IsAdminUser],
            "update": [IsAdminUser],
            "partial_update": [IsAdminUser],
            "destroy": [IsAdminUser],
        }
        return [perm() for perm in permission_map.get(self.action, [IsAdminUser])]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SupportRequest.objects.all()
        # Users can only see their own requests
        return SupportRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="open")

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can update support requests.")

        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Restrict updates to only 'status' field for now
        allowed_fields = {"status"}
        update_data = {
            field: value
            for field, value in request.data.items()
            if field in allowed_fields
        }

        if not update_data:
            raise ValidationError(
                {"detail": "At least one updatable field ('status') must be provided."}
            )

        serializer = self.get_serializer(instance, data=update_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": "Support request updated successfully.",
                "data": serializer.data,
            }
        )

    def partial_update(self, request, *args, **kwargs):
        # Delegate partial_update to update with partial=True
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {
                    "message": "Contact info created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Failed to create contact info.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    "message": "Contact info updated successfully.",
                    "data": serializer.data,
                }
            )
        return Response(
            {"message": "Failed to update contact info.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Contact info deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
