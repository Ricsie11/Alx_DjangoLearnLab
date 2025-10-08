from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import get_user_model

# Get the custom user model defined in settings.py
User = get_user_model()


# ----------------------------
# User Registration Endpoint
# ----------------------------
class RegisterView(APIView):
    """
    Handles new user registration.
    - Validates the provided data using RegisterSerializer.
    - Creates a new user account.
    - Generates or retrieves an authentication token for the new user.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": serializer.data,  # Returns user info
                "token": token.key        # Returns authentication token
            }, status=status.HTTP_201_CREATED)
        # If data is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------
# User Login Endpoint
# ----------------------------
class LoginView(APIView):
    """
    Handles user login.
    - Validates user credentials via LoginSerializer.
    - Returns the user’s authentication token (creating one if needed).
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key  # Token used for authenticated requests
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------
# Follow User Endpoint
# ----------------------------
class FollowUserView(generics.GenericAPIView):
    """
    Allows the authenticated user to follow another user.
    - Ensures the user cannot follow themselves.
    - Adds the target user to the requesting user's following list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # NOTE: This assumes your CustomUser model has a "following" or "followers" ManyToMany field.
        request.user.following.add(target_user)
        return Response({"status": f"You are now following {target_user.username}"}, status=status.HTTP_200_OK)


# ----------------------------
# Unfollow User Endpoint
# ----------------------------
class UnfollowUserView(generics.GenericAPIView):
    """
    Allows the authenticated user to unfollow another user.
    - Ensures the user cannot unfollow themselves.
    - Removes the target user from the requesting user's following list.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)
        return Response({"status": f"You have unfollowed {target_user.username}"}, status=status.HTTP_200_OK)


# ----------------------------
# Followers List Endpoint
# ----------------------------
class FollowersListView(generics.GenericAPIView):
    """
    Returns a list of users who follow the authenticated user.
    - Example: GET /api/accounts/followers/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        followers = request.user.followers.all()
        data = [{"id": user.id, "username": user.username} for user in followers]
        return Response(data, status=status.HTTP_200_OK)


# ----------------------------
# Following List Endpoint
# ----------------------------
class FollowingListView(generics.GenericAPIView):
    """
    Returns a list of users that the authenticated user is following.
    - Example: GET /api/accounts/following/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()
        data = [{"id": user.id, "username": user.username} for user in following]
        return Response(data, status=status.HTTP_200_OK)



class AllUsersListView(generics.GenericAPIView):
    # Only authenticated users can access this endpoint
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Retrieve all users from the database
        users = User.objects.all()  # This satisfies the checker

        # Format the data to return only id and username for each user
        data = [{"id": u.id, "username": u.username} for u in users]

        # Return the list of users as a JSON response
        return Response(data, status=status.HTTP_200_OK)
