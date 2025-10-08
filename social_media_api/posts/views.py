from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import permissions, status

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
