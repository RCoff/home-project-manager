import uuid

from django.shortcuts import render
from django.views import View
from . import forms
from data import models


# Create your views here.
class Index(View):
    template = 'index.html'
    form = forms.CreateProjectsForm()
    context = {'form': form}
    user = None

    def get(self, request):
        if request.user.is_authenticated:
            self.user = request.user
            self.context.update({'properties': self.properties()})

        return render(request, template_name=self.template, context=self.context)

    def properties(self):
        q = models.Properties.objects.filter(users=self.user)
        return q


class PropertyView(View):
    template = 'property.html'
    property = None
    context = {}

    def get(self, request, id):
        self.property = get_property(id)
        self.context.update({'property': self.property,
                             'spaces': self.property.propertyspaces_set.all})

        return render(request, template_name=self.template, context=self.context)


class SpaceView(View):
    template = 'space.html'
    property = None
    space = None
    context = {}

    def get(self, request, property_id, space_id):
        self.property = get_property(property_id)
        self.space = get_space(space_id)

        self.context.update({'property': self.property,
                             'space': self.space,
                             'projects': self.space.projects_set.all,
                             'tasks': self.space.tasks.all})

        return render(request, template_name=self.template, context=self.context)


class CreateProjectView(View):
    template = 'project.html'
    return_url = ""
    context = {}

    def get(self, request):
        return render(request, template_name=self.template, context=self.context)

    def post(self, request):
        pass


def get_space(space_id: uuid.uuid4):
    return models.PropertySpaces.objects.get(id=space_id)


def get_property(property_id: uuid.uuid4):
    return models.Properties.objects.get(id=property_id)
