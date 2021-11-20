from data.models import Properties, PropertySpaces, Tasks, Projects, ProjectAttachments
from django import forms


class AddPropertiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Properties
        fields = ['name', 'address', 'city', 'state']


class AddPropertySpacesForm(forms.ModelForm):
    class Meta:
        model = PropertySpaces
        fields = ['name']


class CreateTasksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_datetime'].widget = forms.DateTimeInput(attrs={'class': 'form-control',
                                                                          'type': 'datetime-local'})
        self.fields['end_datetime'].widget = forms.DateTimeInput(attrs={'class': 'form-control',
                                                                        'type': 'datetime-local'})

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'start_datetime', 'end_datetime']


class CreateProjectsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget = forms.DateInput(attrs={'class': 'form-control',
                                                                  'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'class': 'form-control',
                                                                'type': 'date'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Projects
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'cost', ]
