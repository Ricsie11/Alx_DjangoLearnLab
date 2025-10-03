from rest_framework import serializers
from .models import Post

# Create serializers for Post and Comment models
class PostSeriaalizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'published_date', 'author']