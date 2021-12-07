import logging

import django.db.utils
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from . import forms
from data import models
from home_project_manager import utils

logger = logging.getLogger(__name__)


# TODO: Add (middleware?) authentication verification for properties/projects/etc.


# Create your views here.
class Index(View):
    template = 'index.html'
    form = forms.AddPropertiesForm()
    context = {}
    user = None

    def get(self, request):
        if request.user.is_authenticated:
            self.user = request.user
            self.context.update({'properties': self.properties()})

            if not self.context.get('properties'):
                self.context.update({'form': self.form})
        else:
            self.context.pop('form', None)

        return render(request, template_name=self.template, context=self.context)

    def properties(self):
        q = models.Properties.objects.filter(users=self.user)
        return q


class PropertyView(LoginRequiredMixin, View):
    template = 'property.html'
    property = None
    context = {}

    def get(self, request, id):
        self.property = utils.get_property(id)

        # TODO: Create Permission Denied Page
        utils.check_access(request, self.property)

        self.context.update({'property': self.property,
                             'spaces': self.property.propertyspaces_set.all,
                             'projects': self.property.projects_set.filter(property_space=None)})

        return render(request, template_name=self.template, context=self.context)


class SpaceView(LoginRequiredMixin, View):
    template = 'space.html'
    space = None
    context = {}

    def get(self, request, id):
        self.space = utils.get_space(id)

        # _check_access(request, self.space)

        self.context.update({'property': self.space.property,
                             'space': self.space,
                             'projects': self.space.projects_set.filter(property_space=self.space),
                             'tasks': self.space.tasks.all})

        return render(request, template_name=self.template, context=self.context)


class TaskView(LoginRequiredMixin, View):
    template = "task.html"
    task = None
    context = {}

    def get(self, request, id):
        self.task = utils.get_task(id)
        self.context.update({'task': self.task})

        return render(request, template_name=self.template, context=self.context)


class CreateProjectView(LoginRequiredMixin, View):
    template = 'project_create.html'
    form = forms.CreateProjectsForm()
    return_url = ""
    context = {'form': form}

    def get(self, request, id):
        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        self.form = forms.CreateProjectsForm(request.POST)
        if self.form.is_valid():
            parent = utils.get_parent_object(id)
            if isinstance(parent, models.Properties):
                self.form.instance.property = parent
            elif isinstance(parent, models.PropertySpaces):
                self.form.instance.property = parent.property
                self.form.instance.property_space = parent
            else:
                raise ValueError

            try:
                new_project = self.form.save()
                return HttpResponseRedirect(reverse('project', args=[new_project.id]))
            except django.db.utils.IntegrityError:
                self.context.update({'project_already_exists': "True",
                                     'form': self.form})
                return self.get(request, id)


class CreateTaskView(LoginRequiredMixin, View):
    template = "task_create.html"
    form = forms.CreateTasksForm()
    context = {'form': form}

    def get(self, request, id):
        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        self.form = forms.CreateTasksForm(request.POST)
        if self.form.is_valid():
            parent = utils.get_parent_object(id)
            if isinstance(parent, models.Properties):
                self.form.instance.property = parent
            elif isinstance(parent, models.PropertySpaces):
                self.form.instance.property = parent.property
                self.form.instance.property_space = parent
            else:
                raise ValueError

            try:
                new_task = self.form.save()
                return HttpResponseRedirect(reverse('task', args=[new_task.id]))
            except django.db.utils.IntegrityError:
                self.context.update({'task_already_exists': "True",
                                     'form': self.form})
                return self.get(request, id)


class AddPropertyView(LoginRequiredMixin, View):
    template = 'property_add.html'
    form = forms.AddPropertiesForm()
    context = {'form': form}

    def get(self, request):
        return render(request, template_name=self.template, context=self.context)

    def post(self, request):
        self.form = forms.AddPropertiesForm(request.POST, request.FILES)
        self.context.update({'form': self.form})
        if self.form.is_valid():
            new_property = self.form.save()
            if self.form.cleaned_data['thumbnail']:
                new_image = models.Images(image=self.form.cleaned_data['thumbnail'])
                new_image.save()
                new_property.thumbnail = new_image

            new_property.users.add(request.user)
            new_property.save()

            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, template_name=self.template, context=self.context)


class AddSpaceView(LoginRequiredMixin, View):
    template = 'space_add.html'
    form = forms.AddPropertySpacesForm()
    context = {'form': form}
    property_id = None

    def get(self, request, id):
        self.property_id = id
        self.context.update({'property': utils.get_property(self.property_id)})

        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        self.form = forms.AddPropertySpacesForm(request.POST, request.FILES)
        if self.form.is_valid():
            self.form.instance.property = utils.get_property(id)
            new_space = self.form.save()

            if self.form.cleaned_data['thumbnail']:
                new_image = models.Images(image=self.form.cleaned_data['thumbnail'])
                new_image.save()
                new_space.thumbnail = new_image
                new_space.save()

            return HttpResponseRedirect(reverse('space', args=[new_space.id]))
