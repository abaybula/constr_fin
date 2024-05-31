from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm


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
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

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
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email


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
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

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
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
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

