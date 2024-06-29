from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user.
        Args:
            request (HttpRequest): The HTTP request object.
            username (str): The username to authenticate.
            password (str): The password to authenticate.
            **kwargs: Additional keyword arguments.
        """
        # Get the user model
        user_model = get_user_model()
        # Check if the username is an email address
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password) and user.is_verified:
                return user
        # If the username is not an email address, return None
        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Get a user by ID.
        Args:
            user_id (int): The ID of the user.
        """
        # Get the user model
        user_model = get_user_model()
        # Get the user by ID
        try:
            return user_model.objects.get(pk=user_id)
        # If the user does not exist, return None
        except user_model.DoesNotExist:
            return None
