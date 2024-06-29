import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    """
    Form for logging in a user.
    """
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        """
        Metaclass for LoginUserForm.
        """
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    """
    Form for registering a new user.
    """
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm Password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        """
        Metaclass for RegisterUserForm.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """
        Cleans the email field in the form.
        This method is responsible for validating the email field in the form. It checks if the email already exists in
         the database. If the email is already registered, it raises a `forms.ValidationError` with the message "Email
          already registered". Otherwise, it returns the cleaned email.
        Parameters:
            self (object): The current instance of the form.
        Returns:
            str: The cleaned email.
        Raises:
            forms.ValidationError: If the email is already registered.
        """
        # Get the email from the cleaned data
        email = self.cleaned_data['email']
        # Check if the email already exists in the database
        if get_user_model().objects.filter(email=email).exists():
            # If the email is already registered, raise a ValidationError
            raise forms.ValidationError(_("Email already registered"))
        # Otherwise, return the cleaned email
        return email

    def clean(self):
        """
        Cleans the form data.
        This method is responsible for validating the form data. It checks if the passwords match. If the passwords do
            not match, it raises a `forms.ValidationError` with the message "Passwords do not match". Otherwise, it returns
            the cleaned data.
        Returns:
            dict: The cleaned data.
        Raises:
            forms.ValidationError: If the passwords do not match.
        """
        # Get the cleaned data
        cleaned_data = super().clean()
        # Get the password and confirm password from the cleaned data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # Check if the passwords match
        if password != confirm_password:
            # If the passwords do not match, raise a ValidationError
            raise forms.ValidationError(_("Passwords do not match"))
        # Otherwise, return the cleaned data
        return cleaned_data

    def save(self, commit=True):
        """
        Saves the user to the database.
        This method is responsible for saving the user to the database. It sets the email and verification UUID for the
            user before saving it to the database.
        Parameters:
            commit (bool): A boolean value indicating whether to save the user to the database.
        Returns:
            User: The user object saved to the database.
        """
        # Save the user to the database
        user = super().save(commit=False)
        # Set the email and verification UUID for the user
        user.email = self.cleaned_data['email']
        # Generate a verification UUID for the user
        user.verification_uuid = uuid.uuid4()
        # If commit is True, save the user to the database
        if commit:
            user.save()
        # Return the user object
        return user


class ProfileUserForm(forms.ModelForm):
    """
    Form for editing a user's profile.
    """
    username = forms.CharField(disabled=True, label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='Email', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        """
        Metaclass for ProfileUserForm.
        """
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Cleans the email field in the form.
        This method is responsible for validating the email field in the form. It checks if the email already exists in
         the database. If the email is already registered, it raises a `forms.ValidationError` with the message "Email
          already registered". Otherwise, it returns the cleaned email.
        Parameters:
            self (object): The current instance of the form.
        Returns:
            str: The cleaned email.
        Raises:
            forms.ValidationError: If the email is already registered.
        """
        # Get the email from the cleaned data
        email = self.cleaned_data['email']
        # Check if the email already exists in the database
        if get_user_model().objects.filter(email=email).exists():
            # If the email is already registered, raise a ValidationError
            raise forms.ValidationError(_("Email already registered"))
        # Otherwise, return the cleaned email
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    """
    A form that lets a user change their password.
    """
    old_password = forms.CharField(label='Old Password', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='New Password', max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='Confirm Password', max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        """
        Metaclass for UserPasswordChangeForm.
        """
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')
