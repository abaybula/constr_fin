from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import LoginUserForm, RegisterUserForm


class LoginUserTest(TestCase):
    """
    This class defines the test suite for the `LoginUserForm` form.
    """
    def setUp(self):
        """
        Set up the test environment by creating a test user with the username 'testuser' and the password '1XISRUkwtuK'.
        This method is called before each test case is executed.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='1XISRUkwtuK'
        )

    def test_login_user(self):
        """
        Test the login user form.
        This test case checks if a user can successfully login using the `LoginUserForm` form. It creates a new user
        object with the given username and password. The test then asserts that the `is_valid` method of the form is
        `True`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': 'testuser',
            'password': '1XISRUkwtuK'
        })
        self.assertTrue(form.is_valid())

    def test_login_user_incorrect_username_and_password(self):
        """
        Test the login user form with incorrect username and password.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with incorrect username
        and password. It creates a new form object with the given incorrect username and password. The test then asserts
        that the `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': 'testuser1',
            'password': '1XISRUkwtuK'
        })
        self.assertFalse(form.is_valid())

    def test_login_user_incorrect_username(self):
        """
        Test the login user form with incorrect username.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with an incorrect username.
        It creates a new form object with the given incorrect username and a valid password. The test then asserts that the
        `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': 'testuser1',
            'password': '1XISRUkwtuK'
        })
        self.assertFalse(form.is_valid())

    def test_login_user_incorrect_password(self):
        """
        Test the login user form with incorrect password.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with an incorrect password.
        It creates a new form object with a valid username and an incorrect password. The test then asserts that the
        `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': 'testuser',
            'password': '12345'
        })
        self.assertFalse(form.is_valid())

    def test_login_user_no_username(self):
        """
        Test the login user form with no username.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with no username. It
        creates a new form object with an empty username and a valid password. The test then asserts that the
        `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': '',
            'password': '1XISRUkwtuK'
        })
        self.assertFalse(form.is_valid())

    def test_login_user_no_password(self):
        """
        Test the login user form with no password.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with no password. It
        creates a new form object with a valid username and an empty password. The test then asserts that the
        `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': 'testuser',
            'password': ''
        })
        self.assertFalse(form.is_valid())

    def test_login_user_no_username_and_password(self):
        """
        Test the login user form with no username and password.
        This test case checks if a user cannot successfully login using the `LoginUserForm` form with no username and
        password. It creates a new form object with an empty username and an empty password. The test then asserts that
        the `is_valid` method of the form is `False`.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = LoginUserForm(data={
            'username': '',
            'password': ''
        })
        self.assertFalse(form.is_valid())


class RegisterUserTest(TestCase):
    """
    This class defines the test suite for the `RegisterUserForm` form.
    """
    def setUp(self):
        """
        Set up the test case by creating a user.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='p8qFP@example.com'
        )
        self.user.set_password('1XISRUkwtuK')
        self.user.save()

    def test_register_user(self):
        """
        Test if the form is valid with valid data.
        This test case checks if the form is valid when provided with valid data. It creates a dictionary
        containing user data and initializes a `RegisterUserForm` object with the data. Then, it asserts that
        the form is valid.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        form = RegisterUserForm(data={
            'username': 'testuser1',
            'email': 'p8qFQ@example.com',
            'first_name': 'John',
            'last_name': 'Doo',
            'password1': '1XISRUkwtuK',
            'password2': '1XISRUkwtuK'
        })
        self.assertTrue(form.is_valid(), msg=str(form.errors))
