import unittest
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .forms import ConstructionForm, PositionForm
from .models import Position, Construction


class ConstructionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')
        self.construction = Construction.objects.create(user=self.user, construction='test_construction')

    def test_construction_creation(self):
        self.assertEqual(self.construction.user, self.user)
        self.assertEqual(self.construction.construction, 'test_construction')

    def test_construction_str(self):
        self.assertEqual(str(self.construction), 'test_construction')

    def test_construction_delete(self):
        self.construction.delete()
        self.assertEqual(Construction.objects.count(), 0)

    def test_construction_update(self):
        self.construction.construction = 'updated_construction'
        self.construction.save()
        self.assertEqual(self.construction.construction, 'updated_construction')


class PositionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK', is_staff=True)
        self.construction = Construction.objects.create(user=self.user, construction='test_construction')
        self.position = Position.objects.create(
            construction=self.construction,
            user=self.user,
            order=1,
            name='Test position',
            start_date=date(2022, 1, 1),
            end_date=date(2022, 1, 1),
            cost=100.00
        )

    def test_position_name(self):
        position = Position.objects.get(id=self.position.id)
        field_label = position._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_position_start_date(self):
        position = Position.objects.get(id=self.position.id)
        field_label = position._meta.get_field('start_date').verbose_name
        self.assertEqual(field_label, 'start date')

    def test_position_end_date(self):
        position = Position.objects.get(id=self.position.id)
        field_label = position._meta.get_field('end_date').verbose_name
        self.assertEqual(field_label, 'end date')

    def test_position_cost(self):
        position = Position.objects.get(id=self.position.id)
        field_label = position._meta.get_field('cost').verbose_name
        self.assertEqual(field_label, 'cost')

    def test_position_creation(self):
        self.assertEqual(self.position.construction, self.construction)
        self.assertEqual(self.position.user, self.user)
        self.assertEqual(self.position.order, 1)
        self.assertEqual(self.position.name, 'Test position')
        self.assertEqual(self.position.start_date, date(2022, 1, 1))
        self.assertEqual(self.position.end_date, date(2022, 1, 1))
        self.assertEqual(self.position.cost, 100.00)

    def test_position_str(self):
        position = Position.objects.get(id=self.position.id)
        self.assertEqual(str(position), 'Test position')

    def test_position_delete(self):
        self.position.delete()
        self.assertEqual(Position.objects.count(), 0)

    def test_position_update(self):
        self.position.name = 'Updated position'
        self.position.save()
        self.assertEqual(self.position.name, 'Updated position')

    def test_position_order(self):
        self.position.order = 2
        self.position.save()
        self.assertEqual(self.position.order, 2)

    def test_position_other_name(self):
        self.position.name = 'other'
        self.position.save()
        self.assertEqual(self.position.name, 'other')


class ConstructionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')

    def test_construction_form_valid_data(self):
        form = ConstructionForm(self.user, data={'construction': 'New Building'})
        self.assertTrue(form.is_valid())

    def test_construction_form_no_data(self):
        form = ConstructionForm(self.user, data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_construction_form_widgets(self):
        form = ConstructionForm(self.user)
        self.assertIn('class="form-input"', str(form['construction']))


class PositionFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1XISRUkwtuK')
        self.construction = Construction.objects.create(user=self.user, construction='New Construction')

    def test_position_form_valid_data(self):
        form = PositionForm(
            self.user, self.construction.id,
            data={
                'order': 1,
                'name': 'Foundation',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'cost': 10000,
                'other_name': ''
            }
        )
        self.assertTrue(form.is_valid())

    def test_position_form_invalid_date(self):
        form = PositionForm(
            self.user, self.construction.id,
            data={
                'order': 1,
                'name': 'Foundation',
                'start_date': '2023-12-31',
                'end_date': '2023-01-01',
                'cost': 10000,
                'other_name': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('End date cannot be earlier than start date.', form.errors['__all__'])

    def test_position_form_other_name_required(self):
        form = PositionForm(
            self.user, self.construction.id,
            data={
                'order': 1,
                'name': 'other',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'cost': 10000,
                'other_name': ''
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('Please provide a value for other name', form.errors['other_name'])

    def test_position_form_widgets(self):
        form = PositionForm(self.user, self.construction.id)
        self.assertIn('type="number"', str(form['order']))
        self.assertIn('type="date"', str(form['start_date']))
        self.assertIn('type="date"', str(form['end_date']))

    def test_position_form_save(self):
        form = PositionForm(
            self.user, self.construction.id,
            data={
                'order': 1,
                'name': 'other',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'cost': 10000,
                'other_name': 'Custom Work'
            }
        )
        self.assertTrue(form.is_valid())
        position = form.save(commit=True)
        self.assertEqual(position.name, 'Custom Work')
        self.assertEqual(position.user, self.user)
        self.assertEqual(position.construction_id, self.construction.id)


if __name__ == '__main__':
    unittest.main()


class IndexViewTest(TestCase):
    def test_index_view_get(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class ConstructionListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.url = reverse('constructions_list', args=[self.user.id])

    def test_construction_list_view_permission_denied(self):
        other_user = User.objects.create_user(username='otheruser', password='54321')
        response = self.client.get(reverse('constructions_list', args=[other_user.id]))
        self.assertEqual(response.status_code, 403)

    def test_construction_list_view_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constructions_list.html')


class AddConstructionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.url = reverse('add_construction', args=[self.user.id])

    def test_add_construction_view_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_construction.html')


class EditConstructionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.construction = Construction.objects.create(user=self.user, construction='Existing Construction')
        self.url = reverse('edit_construction', args=[self.user.id, self.construction.id])

    def test_edit_construction_view_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_construction.html')

    def test_edit_construction_view_post_success(self):
        response = self.client.post(self.url, {'construction': 'Updated Construction'})
        self.assertEqual(response.status_code, 302)
        self.construction.refresh_from_db()
        self.assertEqual(self.construction.construction, 'Updated Construction')


class DeleteConstructionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.construction = Construction.objects.create(user=self.user, construction='Existing Construction')
        self.url = reverse('delete_construction', args=[self.user.id, self.construction.id])

    def test_delete_construction_view_get_permission_denied(self):
        other_user = User.objects.create_user(username='otheruser', password='54321')
        response = self.client.get(reverse('delete_construction', args=[other_user.id, self.construction.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_construction_view_get_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_construction.html')

    def test_delete_construction_view_post_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Construction.objects.filter(id=self.construction.id).exists())
