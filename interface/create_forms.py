from data.models import Properties, PropertySpaces, Tasks
from project.models import Projects, ProjectAttachments, ProjectActionItem
from django import forms


class AddPropertiesForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)
    include_defaults = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['zipcode'].widget = forms.NumberInput(attrs={'class': 'form-control'})
        self.fields['thumbnail'].widget.attrs.update({'class': 'form-control'})
        self.fields['include_defaults'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['include_defaults'].initial = True

    class Meta:
        model = Properties
        fields = ['name', 'address', 'city', 'state', 'zipcode']


class AddPropertySpacesForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['thumbnail'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = PropertySpaces
        fields = ['name']


class CreateActionItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ProjectActionItem
        fields = ['title', 'description']


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
