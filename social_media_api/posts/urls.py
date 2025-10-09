from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikeViewSet

# Create a router to automatically generate routes for our ViewSets
router = DefaultRouter()

# Register the Post and Comment viewsets with the router
# This automatically creates endpoints like:
# /posts/  -> list and create posts
# /posts/<id>/  -> retrieve, update, or delete a post
# /comments/  -> list and create comments
# /comments/<id>/  -> retrieve, update, or delete a comment
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

# Define the URL patterns for the app
urlpatterns = [
    # Include all automatically generated routes from the router
    path('', include(router.urls)),

    # Custom route for the user's personalized feed
    # GET /feed/  -> returns posts from users the authenticated user follows
    path('feed/', FeedView.as_view(), name='user-feed'),

     # Like system routes
    path('posts/<int:post_id>/like/', LikeViewSet.as_view({'post': 'create'}), name='like-post'),
    path('posts/<int:post_id>/unlike/', LikeViewSet.as_view({'delete': 'destroy'}), name='unlike-post'),
]
