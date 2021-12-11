from django import forms

from project import models


class AddMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control',
                                                        'rows': 3})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.ProjectMaterial
        fields = ['url', 'name', 'description', 'quantity', 'cost']
