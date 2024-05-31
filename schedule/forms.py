from django import forms
from django.utils.translation import gettext_lazy as _
from schedule.models import Position, Construction


class ConstructionForm(forms.ModelForm):
    """ Construction form - used to store construction names. """
    class Meta:
        model = Construction
        fields = ['construction_name']


class PositionForm(forms.ModelForm):
    """ Position form - used to store positions. """
    other_name = forms.CharField(max_length=100, required=False, label=_('Other name'))

    class Meta:
        """ Metaclass for Position form. """
        model = Position
        fields = ['order', 'name', 'start_date', 'end_date', 'cost']
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
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'cost': forms.NumberInput(attrs={'type': 'cost'}),
        }

    def clean(self):
        """
        Validates the form data.
        Parameters:
            None
        Returns:
            dict: The cleaned form data.
        Raises:
            None
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        other_name = cleaned_data.get('other_name')

        if name == 'other' and not other_name:
            self.add_error('other_name', _('Please provide a value for other name'))

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError(_("End date cannot be earlier than start date."))

        return cleaned_data

    def save(self, commit=True):
        """
        Saves the form data to the database.
        Parameters:
            commit (bool): Whether to save the changes to the database. Defaults to True.
        Returns:
            Position: The saved Position object.
        Raises:
            None
        """
        position = super().save(commit=False)
        if self.cleaned_data['name'] == 'other':
            position.name = self.cleaned_data['other_name']
        if commit:
            position.save()
        return position

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the given arguments and keyword arguments.
        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            None
        This method calls the parent class's __init__ method with the given arguments and keyword arguments.
        It then sets the 'required' attribute of the 'other_name' field to False.
        """
        super().__init__(*args, **kwargs)
        self.fields['other_name'].required = False

