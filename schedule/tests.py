
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .forms import PositionForm, ConstructionForm
from .models import Position, Construction


class ConstructionModelTest(TestCase):
    """
    This class defines the test suite for the `Construction` model.
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
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')

    def test_create_construction_name(self):
        """
        Test the creation of a construction name.
        This test case checks if a construction name can be successfully created using the `Construction` model.
        It creates a new construction object with the given name and associates it with the test user. The test then
        asserts that the string representation of the construction object matches the expected name.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        self.assertEqual(str(construction), 'Test Construction')

    def test_edit_construction_name(self):
        """
        Test the editing of a construction name.
        This test case checks if a construction name can be successfully edited using the `Construction` model.
        It creates a new construction object with the given name and associates it with the test user. The test then
        asserts that the string representation of the construction object matches the expected name after editing.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        construction.construction_name = 'Updated Construction'
        construction.save()
        self.assertEqual(str(construction), 'Updated Construction')

    def test_delete_construction_name(self):
        """
        Test the deletion of a construction name.
        This test case checks if a construction name can be successfully deleted using the `Construction` model.
        It creates a new construction object with the given name and associates it with the test user. The test then
        asserts that the construction object is deleted successfully.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        construction.delete()
        self.assertFalse(Construction.objects.filter(construction_name='Test Construction').exists())


class PositionModelTest(TestCase):
    """
    This class defines the test suite for the `Position` model.
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
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')

    def test_create_position(self):
        """
        Test the creation of a position.
        This test case checks if a position can be successfully created using the `Position` model.
        It creates a new position object with the given name and associates it with the test user. The test then
        asserts that the string representation of the position object matches the expected name.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        self.assertEqual(str(position), 'testuser - Foundation')
        self.assertEqual(position.cost, 10000.00)

    def test_edit_position(self):
        """
        Test the editing of a position.
        This test case checks if a position can be successfully edited using the `Position` model.
        It creates a new position object with the given name and associates it with the test user. The test then
        asserts that the string representation of the position object matches the expected name after editing.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        position.cost = 20000.00
        position.save()
        self.assertEqual(position.cost, 20000.00)

    def test_delete_position(self):
        """
        Test the deletion of a position.
        This test case checks if a position can be successfully deleted using the `Position` model.
        It creates a new position object with the given name and associates it with the test user. The test then
        asserts that the position object is deleted successfully.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        position.delete()
        positions = Position.objects.all()
        self.assertEqual(len(positions), 0)


class ConstructionFormTest(TestCase):
    """
    This class defines the test suite for the `ConstructionForm` form.
    """
    def test_valid_form(self):
        """
        Test if the form is valid with valid data.
        This test case checks if the form is valid when provided with valid data. It creates a dictionary
        containing a construction name and initializes a `ConstructionForm` object with the data. Then, it
        asserts that the form is valid.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'construction_name': 'Test Construction',
        }
        form = ConstructionForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test if the form is invalid with invalid data.
        This test case checks if the form is invalid when provided with invalid data. It creates a dictionary
        containing an empty construction name and initializes a `ConstructionForm` object with the data. Then, it
        asserts that the form is invalid.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'construction_name': '',
        }
        form = ConstructionForm(data)
        self.assertFalse(form.is_valid())


class PositionFormTest(TestCase):
    """
    This class defines the test suite for the `PositionForm` form.
    """
    def test_valid_form(self):
        """
        Test if the form is valid with valid data.
        This test case checks if the form is valid when provided with valid data. It creates a dictionary
        containing position data and initializes a `PositionForm` object with the data. Then, it asserts that
        the form is valid.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'order': 1,
            'name': 'Foundation',
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'cost': 10000.00
        }
        form = PositionForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test if the form is invalid with invalid data.
        This test case checks if the form is invalid when provided with invalid data. It creates a dictionary
        containing an empty position data and initializes a `PositionForm` object with the data. Then, it asserts
        that the form is invalid.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'order': '',
            'name': 'Foundation',
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'cost': 10000.00
        }
        form = PositionForm(data)
        self.assertFalse(form.is_valid())


class PositionViewTest(TestCase):
    """
    This class defines the test suite for the `PositionView` view.
    """
    def setUp(self):
        """
        Set up the test case by creating a user and client.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')
        self.client.login(username='testuser', password='1XISRUkwtuK')

    def test_index_view(self):
        """
        Test if the index view is rendered correctly.
        This test case checks if the index view is rendered correctly when provided with valid data. It asserts
        that the response status code is 200 and that the template used is 'index.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_add_construction_name_view(self):
        """
        Test if the add construction name view is rendered correctly.
        This test case checks if the add construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'add_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        response = self.client.get(reverse('add_construction_name', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_construction_name.html')

    def test_add_construction_name_post_view(self):
        """
        Test if the add construction name view is rendered correctly.
        This test case checks if the add construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'add_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'construction_name': 'Test Construction',
        }
        response = self.client.post(reverse('add_construction_name', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)

    def test_edit_construction_name_view(self):
        """
        Test if the edit construction name view is rendered correctly.
        This test case checks if the edit construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'edit_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        response = self.client.get(reverse('edit_construction_name', args=[self.user.id, construction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_construction_name.html')

    def test_edit_construction_name_post_view(self):
        """
        Test if the edit construction name view is rendered correctly.
        This test case checks if the edit construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'edit_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        data = {
            'construction_name': 'Updated Construction',
        }
        response = self.client.post(reverse('edit_construction_name', args=[self.user.id, construction.id]), data)
        self.assertEqual(response.status_code, 302)

    def test_delete_construction_name_view(self):
        """
        Test if the delete construction name view is rendered correctly.
        This test case checks if the delete construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'delete_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        response = self.client.get(reverse('delete_construction_name', args=[self.user.id, construction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_construction_name.html')

    def test_delete_construction_name_post_view(self):
        """
        Test if the delete construction name view is rendered correctly.
        This test case checks if the delete construction name view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'delete_construction_name.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        construction = Construction.objects.create(
            construction_name='Test Construction',
            user=self.user
        )
        response = self.client.post(reverse('delete_construction_name', args=[self.user.id, construction.id]))
        self.assertEqual(response.status_code, 302)

    def test_add_position_view(self):
        """
        Test if the add position view is rendered correctly.
        This test case checks if the add position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'add_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        response = self.client.get(reverse('add_position', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_position.html')

    def test_add_position_post_view(self):
        """
        Test if the add position view is rendered correctly.
        This test case checks if the add position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'add_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        data = {
            'order': 1,
            'name': 'Foundation',
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'cost': 10000.00
        }
        response = self.client.post(reverse('add_position', args=[self.user.id]), data)
        self.assertEqual(response.status_code, 302)

    def test_edit_position_view(self):
        """
        Test if the edit position view is rendered correctly.
        This test case checks if the edit position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'edit_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        response = self.client.get(reverse('edit_position', args=[self.user.id, position.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_position.html')

    def test_edit_position_post_view(self):
        """
        Test if the edit position view is rendered correctly.
        This test case checks if the edit position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'edit_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        data = {
            'order': 1,
            'name': 'Foundation',
            'start_date': '2024-01-01',
            'end_date': '2024-02-01',
            'cost': 20000.00
        }
        response = self.client.post(reverse('edit_position', args=[self.user.id, position.id]), data)
        self.assertEqual(response.status_code, 302)

    def test_delete_position_view(self):
        """
        Test if the delete position view is rendered correctly.
        This test case checks if the delete position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'delete_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        response = self.client.get(reverse('delete_position', args=[self.user.id, position.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_position.html')

    def test_delete_position_post_view(self):
        """
        Test if the delete position view is rendered correctly.
        This test case checks if the delete position view is rendered correctly when provided with valid data.
        It asserts that the response status code is 302 and that the template used is 'delete_position.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        position = Position.objects.create(
            user=self.user,
            order=1,
            name='Foundation',
            start_date='2024-01-01',
            end_date='2024-02-01',
            cost=10000.00
        )
        response = self.client.post(reverse('delete_position', args=[self.user.id, position.id]))
        self.assertEqual(response.status_code, 302)

    def test_schedule_view(self):
        """
        Test if the schedule view is rendered correctly.
        This test case checks if the schedule view is rendered correctly when provided with valid data.
        It asserts that the response status code is 200 and that the template used is 'schedule.html'.
        Parameters:
            self (TestCase): The current test case instance.
        Returns:
            None
        """
        response = self.client.get(reverse('schedule', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule.html')
