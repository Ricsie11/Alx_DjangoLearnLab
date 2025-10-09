from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.response import Response
from notifications.models import Notification


# ----------------------------
# ViewSets for Post and Comment models
# ----------------------------

# Handles all CRUD operations for Post model (list, retrieve, create, update, delete)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Enables search functionality for posts (search by title or content)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    # Automatically assigns the currently logged-in user as the post author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Handles CRUD operations for Comment model
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    # Enables searching through comments
    # Note: 'post_title' doesn’t exist as a field—this should be 'post__title' if you want to search comments by post title.
    filter_backends = [SearchFilter]
    search_fields = ['content', 'post__title']

    # Automatically assigns the currently logged-in user as the comment author
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------
# Feed view - shows posts from users the current user follows
# ----------------------------
class FeedView(APIView):
    # Ensures only authenticated users can access the feed
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all users that the current user is following
        following_users = request.user.following.all()

        # Retrieve all posts made by followed users, ordered from newest to oldest
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # Serialize and return the posts as JSON response
        serializer = PostSerializer(feed_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# ----------------------------
# Like and Unlike functionality with Notifications
# ----------------------------

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import Post, Like
from .serializers import LikeSerializer
from notifications.models import Notification

class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        """
        Handle liking a post.
        If the post doesn’t exist -> 404.
        If the like already exists -> return message.
        Otherwise, create a like and a notification.
        """
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({'detail': 'You already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Handle unliking a post.
        """
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        Notification.objects.filter(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target_object_id=post.id
        ).delete()

        return Response({'detail': 'Post unliked successfully.'}, status=status.HTTP_200_OK)