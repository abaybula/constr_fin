from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from schedule.models import Position, Construction


class ConstructionForm(forms.ModelForm):
    """
    Form for creating a construction.
    """
    class Meta:
        """
        Meta class for ConstructionForm.
        Args:
            model (Construction): The model associated with the form.
            fields (list): The fields to include in the form.
            widgets (dict): The widgets to use for the form.
        """
        model = Construction
        fields = ['construction']
        widgets = {
            'construction': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, user, *args, **kwargs):
        """
        Initialize the form with the associated user.
        Args:
            user (User): The user associated with the form.
            *args: The positional arguments.
            **kwargs: The keyword arguments.
        """
        # Call the parent class's __init__ method with the provided arguments.
        super().__init__(*args, **kwargs)

        # Store the user associated with the form.
        self.user = user

    def save(self, commit=True):
        """
        Save the construction.
        Args:
            commit (bool): Whether to save the changes to the database.
        Returns:
            Construction: The saved construction object.
        """
        # Create a new construction object
        construction = super().save(commit=False)
        # Set the user attribute of the construction object
        construction.user = self.user
        # If commit is True, save the changes to the database
        if commit:
            construction.save()
        # Return the saved construction object
        return construction


class PositionForm(forms.ModelForm):
    """
    Form for creating a position.
    """
    # Define the other_name field as a CharField with a maximum length of 100.
    other_name = forms.CharField(max_length=100, required=False, label=_('Other name'))

    class Meta:
        """
        Meta class for PositionForm.
        Args:
            model (Position): The model associated with the form.
            fields (list): The fields to include in the form.
            widgets (dict): The widgets to use for the form.
        """
        # Define the model to use for the form.
        model = Position
        # Define the fields to include in the form.
        fields = ['order', 'name', 'start_date', 'end_date', 'cost']
        # Define the widgets to use for the form.
        widgets = {
            'order': forms.NumberInput(attrs={'type': 'number'}),
            'name': forms.Select(choices=[
                ('Preparatory works', _('Preparatory works')),
                ('Foundation', _('Foundation')),
                ('Monolithic works', _('Monolithic works')),
                ('Masonry works', _('Masonry works')),
                ('Windows', _('Windows')),
                ('Roof', _('Roof')),
                ('Doors', _('Doors')),
                ('Decoration', _('Decoration')),
                ('Ebbs, eaves, covers', _('Ebbs, eaves, covers')),
                ('Metal products', _('Metal products')),
                ('Elevators', _('Elevators')),
                ('Facade, insulation', _('Facade, insulation')),
                ('Grounding, lightning protection', _('Grounding, lightning protection')),
                ('Internal power supply', _('Internal power supply')),
                ('Low current networks', _('Low current networks')),
                ('Internal sewerage K1', _('Internal sewerage K1')),
                ('Internal sewerage K2', _('Internal sewerage K2')),
                ('Internal water supply B1', _('Internal water supply B1')),
                ('Gas supply, boilers', _('Gas supply, boilers')),
                ('External power supply', _('External power supply')),
                ('External gas supply', _('External gas supply')),
                ('External sewerage K1', _('External sewerage K1')),
                ('External sewerage K2', _('External sewerage K2')),
                ('External water supply B1', _('External water supply B1')),
                ('Improvement', _('Improvement')),
                ('Total expenditures', _('Total expenditures')),
                ('other', _('Other')),
            ]),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'cost': forms.NumberInput(attrs={'type': 'cost'}),
        }

    def __init__(self, user, construction_id, *args, **kwargs):
        """
        Initialize the PositionForm with the associated user and construction_id.
        Args:
            user (User): The user associated with the form.
            construction_id (int): The id of the construction associated with the form.
            *args: The positional arguments.
            **kwargs: The keyword arguments.
        """
        # Call the parent class's __init__ method with the provided arguments.
        super().__init__(*args, **kwargs)

        # Store the user associated with the form.
        self.user = user

        # Store the construction_id associated with the form.
        self.construction_id = construction_id

    def clean(self):
        """
        This method cleans and validates the form data.
        Ensures uniqueness of position number and name for a construction.
        Validates start and end dates.
        Returns:
            cleaned_data (dict): The cleaned form data.
        """
        cleaned_data = super().clean()
        # Get form data
        order = cleaned_data.get("order")
        name = cleaned_data.get('name')
        other_name = cleaned_data.get('other_name')

        # Get position ID
        if self.instance.pk:
            position_id = self.instance.pk
        else:
            position_id = None

        # Check position number uniqueness
        if Position.objects.filter(construction_id=self.construction_id, order=order).exclude(id=position_id).exists():
            raise ValidationError(_("Position number must be unique for this construction."))

        # Check 'other' name and other_name value
        if name == 'other' and not other_name:
            self.add_error('other_name', _('Please provide a value for other name'))

        # Check position name uniqueness
        if Position.objects.filter(construction_id=self.construction_id, name=name).exclude(id=position_id).exists():
            raise ValidationError(_("Position name must be unique for this construction."))

        # Check start and end date validity
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("End date cannot be earlier than start date."))

        return cleaned_data

    def save(self, commit=True):
        """
        Save the form data to the database.
        Args:
            commit (bool): Whether to save the changes to the database.
        Returns:
            Position: The saved position object.
        """
        # Create a new position object
        position = super().save(commit=False)

        # If the name is 'other', set the name to the value of other_name
        if self.cleaned_data['name'] == 'other':
            position.name = self.cleaned_data['other_name']

        # Set the user and construction_id attributes of the position object
        position.user = self.user
        position.construction_id = self.construction_id

        # If commit is True, save the changes to the database
        if commit:
            position.save()

        # Return the saved position object
        return position
