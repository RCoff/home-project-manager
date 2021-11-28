import logging
import uuid

import django.db.utils
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from . import forms
from data import models


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

    def post(self, request):
        self.form = forms.AddPropertiesForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            self.form.instance.users.add(request.user)
            self.form.save()

        return HttpResponseRedirect(reverse('home'))

    def properties(self):
        q = models.Properties.objects.filter(users=self.user)
        return q


class PropertyView(LoginRequiredMixin, View):
    template = 'property.html'
    property = None
    context = {}

    def get(self, request, id):
        self.property = get_property(id)

        # TODO: Create Permission Denied Page
        _check_access(request, self.property)

        self.context.update({'property': self.property,
                             'spaces': self.property.propertyspaces_set.all,
                             'projects': self.property.projects_set.filter(property_space=None)})

        return render(request, template_name=self.template, context=self.context)


class SpaceView(LoginRequiredMixin, View):
    template = 'space.html'
    space = None
    context = {}

    def get(self, request, id):
        self.space = get_space(id)

        # _check_access(request, self.space)

        self.context.update({'property': self.space.property,
                             'space': self.space,
                             'projects': self.space.projects_set.filter(property_space=self.space),
                             'tasks': self.space.tasks.all})

        return render(request, template_name=self.template, context=self.context)


class ProjectView(LoginRequiredMixin, View):
    template = "project.html"
    project = None
    context = {}

    def get(self, request, id):
        self.project = get_project(id)
        form = forms.CreateProjectsForm(instance=self.project)
        self.context.update({'project': self.project,
                             'form': form})

        _check_access(request, self.project.property)

        return render(request, template_name=self.template, context=self.context)


class TaskView(LoginRequiredMixin, View):
    template = "task.html"
    task = None
    context = {}

    def get(self, request, id):
        self.task = get_task(id)
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
            parent = get_parent_object(id)
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


class CreateActionItem(LoginRequiredMixin, View):
    template = 'project_action_item_add.html'
    context = {}

    def get(self, request, id):
        form = forms.CreateActionItemForm()
        self.context.update({'form': form,
                             'project': get_project(id)})

        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        form = forms.CreateActionItemForm(request.POST)
        if form.is_valid():
            project = get_project(id)
            new_action_item = form.save()
            project.action_items.add(new_action_item)
            project.save()

            return HttpResponseRedirect(reverse('project', args=[id]))

        self.context.update({'form': form})
        return render(request, template_name=self.template, context=self.context)


class CreateTaskView(LoginRequiredMixin, View):
    template = "task_create.html"
    form = forms.CreateTasksForm()
    context = {'form': form}

    def get(self, request, id):
        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        self.form = forms.CreateTasksForm(request.POST)
        if self.form.is_valid():
            parent = get_parent_object(id)
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


class AddSpaceView(LoginRequiredMixin, View):
    template = 'space_add.html'
    form = forms.AddPropertySpacesForm()
    context = {'form': form}
    property_id = None

    def get(self, request, id):
        self.property_id = id
        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        self.form = forms.AddPropertySpacesForm(request.POST)
        if self.form.is_valid():
            self.form.instance.property = get_property(id)
            new_space = self.form.save()

            return HttpResponseRedirect(reverse('space', args=[new_space.id]))


def get_space(space_id: uuid.uuid4):
    return models.PropertySpaces.objects.get(id=space_id)


def get_property(property_id: uuid.uuid4):
    return models.Properties.objects.get(id=property_id)


def get_project(project_id: uuid.uuid4):
    return models.Projects.objects.get(id=project_id)


def get_task(task_id: uuid.uuid4):
    return models.Tasks.objects.get(id=task_id)


def _check_access(request, model_object):
    if request.user not in model_object.users.all():
        raise PermissionDenied


def get_parent_object(id: uuid.uuid4):
    try:
        parent = models.Properties.objects.get(id=id)
    except models.Properties.DoesNotExist:
        parent = models.PropertySpaces.objects.get(id=id)
    return parent
