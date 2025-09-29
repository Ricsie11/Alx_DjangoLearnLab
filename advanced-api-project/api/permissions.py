from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermissions):
    def has_permissions(self, request, view):
        if request.method iin permission.SAFE_METHODS:
            return True
        return request.user.is_staff