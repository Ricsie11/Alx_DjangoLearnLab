from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to allow users to view their notifications.
    - Only authenticated users can access this.
    - Returns notifications for the logged-in user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the notifications meant for the logged-in user
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
