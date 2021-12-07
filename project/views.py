import logging
import uuid

import django.db.utils
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from interface import forms
from . import models
from home_project_manager import utils


class ProjectView(LoginRequiredMixin, View):
    template = "project.html"
    project = None
    context = {}

    def get(self, request, id):
        self.project = utils.get_project(id)
        form = forms.CreateProjectsForm(instance=self.project)
        self.context.update({'project': self.project,
                             'form': form})

        utils.check_access(request, self.project.property)

        return render(request, template_name=self.template, context=self.context)


class CreateActionItem(LoginRequiredMixin, View):
    template = 'project_action_item_add.html'
    context = {}

    def get(self, request, id):
        form = forms.CreateActionItemForm()
        self.context.update({'form': form,
                             'project': utils.get_project(id)})

        return render(request, template_name=self.template, context=self.context)

    def post(self, request, id):
        form = forms.CreateActionItemForm(request.POST)
        if form.is_valid():
            project = utils.get_project(id)
            new_action_item = form.save()
            project.action_items.add(new_action_item)
            project.save()

            return HttpResponseRedirect(reverse('project', args=[id]))

        self.context.update({'form': form})
        return render(request, template_name=self.template, context=self.context)
