from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """
    Allow user to edit their own profile
    """

    # To define permission classes, we define has_object_permission function. 
    # This get called every time the request is made to the api that we assign the permission class to.
    def has_object_permission(self, request, view, obj):
        """
        Check user is trying to edit their own profile
        """
        # We are going to check the method that made for request, whether it is Safe or not. 
        # Safe_methods are methods don't made any change to object (HTTP GET, etc...).
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # If this is not safe method, we check whether user has permission to update or not.
        # The obj is profile obj, we check if obj.id == request.user.id
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """
    Allow users to update their own status
    """

    def has_object_permission(self, request, view, obj):
        """
        Check the user is trying to update their own status
        """
        if request.method == permissions.SAFE_METHODS:
            return True

        # Check if user is updating their own status
        return obj.user_profile.id == request.user.id