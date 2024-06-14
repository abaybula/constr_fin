from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailAuthBackend(BaseBackend):
    """
    Authenticates a user based on their email address.
    Parameters:
        None
    Returns:
        User: The authenticated user object.
    Raises:
        None
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates a user based on the provided credentials.
        Parameters:
            request (HttpRequest): The HTTP request object.
            username (str): The email of the user.
            password (str): The password of the user.
            **kwargs: Additional keyword arguments.
        Returns:
            User: The authenticated user object.
        Raises:
            None
        """
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        """
        Retrieves a user based on the provided user ID.
        Parameters:
            user_id (int): The ID of the user.
        Returns:
            User: The user object if found, otherwise None.
        Raises:
            None
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
