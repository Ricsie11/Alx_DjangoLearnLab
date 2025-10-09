from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    Converts Notification objects to JSON format for API responses.
    """
    actor = serializers.StringRelatedField()      # shows actor's username instead of ID
    recipient = serializers.StringRelatedField()  # shows recipient's username instead of ID
    target = serializers.StringRelatedField()     # shows a readable name of the target (post, comment, etc.)

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']