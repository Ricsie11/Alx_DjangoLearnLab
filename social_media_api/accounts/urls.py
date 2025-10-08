from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    FollowUserView, 
    UnfollowUserView, 
    FollowersListView, 
    FollowingListView
)

# -------------------------------------
# URL patterns for user account actions
# -------------------------------------
urlpatterns = [
    # Endpoint for user registration
    # Example: POST /api/accounts/register/
    path('register/', RegisterView.as_view(), name="register"),

    # Endpoint for user login (authentication)
    # Example: POST /api/accounts/login/
    path('login/', LoginView.as_view(), name="Login"),

    # Endpoint for following another user by ID
    # Example: POST /api/accounts/follow/5/
    # The <int:user_id> part captures the ID of the user to follow
    path('follow/<int:user_id>/', FollowUserView.as_view(), name="follow-user"),

    # Endpoint for unfollowing another user by ID
    # Example: POST /api/accounts/unfollow/5/
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name="unfollow-user"),

    # Endpoint to get a list of all users following the current user
    # Example: GET /api/accounts/followers/
    path('followers/', FollowersListView.as_view(), name='followers-list'),

    # Endpoint to get a list of all users that the current user follows
    # Example: GET /api/accounts/following/
    path('following/', FollowingListView.as_view(), name='following-list'),
]
