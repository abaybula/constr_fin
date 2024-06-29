from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from rest_framework.views import APIView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm

User = get_user_model()


class RegisterUser(CreateView):
    """
    View for user registration.
    """
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Register'}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Handles the form validation for user registration.
        :param form: The form object.
        :return: The response object.
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Define the email subject
        mail_subject = 'Email Verification'

        # Generate the uid and token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Generate the email verification link
        email_verification_link = self.request.build_absolute_uri(
            reverse('users:email_verification_confirm', args=[uid, token])
        )

        # Create the email message
        message = render_to_string('users/active_email.html', {
            'user': user,
            'email_verification_link': email_verification_link,
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

        return render(self.request, 'users/register_done.html')


class EmailVerificationRequest(APIView):
    """
    View for email verification request.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the GET request for email verification request.
        :param request: The request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response object.
        """
        return render(request, 'users/confirm_email.html')


class EmailVerificationConfirm(APIView):
    """
    View for email verification confirmation.
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        """
        Handles the GET request for email verification confirmation.
        :param request: The request object.
        :param uidb64: The base64-encoded user ID.
        :param token: The token for email verification.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response object.
        """
        # Decode the user ID
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # Check if the user is not None and the token is valid
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
        # Return the response object based on the user activation status
            return render(request, 'users/activation_success.html')
        else:
            return render(request, 'users/activation_invalid.html')


class ResendEmail(APIView):
    """
    View for resending the email verification email.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the GET request for resending the email verification email.
        :param request: The request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response object.
        """
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Redirect to the login page if the user is not authenticated
            return redirect('users:login')

        # Get the user
        user = request.user

        # Check if the user is not active
        if not user.is_active:
            # Define the email subject
            mail_subject = 'Email Verification'

            # Generate the uid and token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Generate the email verification link
            email_verification_link = request.build_absolute_uri(
                reverse('users:email_verification_confirm', args=[uid, token])
            )

            # Create the email message
            message = render_to_string('users/active_email.html', {
                'user': user,
                'email_verification_link': email_verification_link,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

        return render(request, 'users/resend_email_done.html')


class ResendEmailDone(APIView):
    """
    View for resending the email verification email done.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the GET request for resending the email verification email done.
        :param request: The request object.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        :return: The response object.
        """
        return render(request, 'users/resend_email_done.html')


class LoginUser(LoginView):
    """
    View for user login.
    """
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login'}


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
