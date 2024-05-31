from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    """
    View for user login.
    """
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}


class RegisterUser(CreateView):
    """
    View for user registration.
    """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Register'}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    """
    View for user profile update.
    """
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile'}

    def get_success_url(self):
        """
        Returns the success URL for the current user profile.
        :return: A string representing the success URL for the user profile.
        """
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Returns the current user object.
        :param queryset: An optional queryset to filter the user object.
        :return: The current user object.
        """
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """
    View for user password change.
    """
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
