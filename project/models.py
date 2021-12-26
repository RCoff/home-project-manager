import uuid

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

from data.models import Images, Properties, PropertySpaces
from .utils import money_fmt

property_ = property


# Create your models here.
class ProjectActionItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(Images, blank=True)


class Projects(models.Model):
    status_choices = (
        ('pl', 'Planning'),
        ('ns', 'Not Started'),
        ('ip', 'In Progress'),
        ('cm', 'Completed'),
        ('hl', 'On Hold'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Properties, null=False, on_delete=models.CASCADE)
    property_space = models.ForeignKey(PropertySpaces, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=2, default='pl')
    cost = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    images = models.ManyToManyField(Images, blank=True)
    shared_users = models.ManyToManyField(User, blank=True)
    action_items = models.ManyToManyField(ProjectActionItem, blank=True)

    class Meta:
        unique_together = ['property', 'property_space', 'name']

    @property_
    def display_cost(self):
        return f"${self.cost:,}"

    @property_
    def url(self):
        return reverse('project', args=[self.id])

    def __str__(self):
        if self.property_space:
            return f"{self.property.name} - {self.property_space.name} - {self.name} ({self.id})"
        else:
            return f"{self.property.name} - Home - {self.name} ({self.id})"


class ProjectAttachments(models.Model):
    CHOICES = (
        ('db', 'DropBox'),
        ('od', 'OneDrive'),
        ('sp', 'SharePoint'),
        ('gd', 'GoogleDrive'),
        ('wa', 'URL'),
        ('im', 'Image'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=2, choices=CHOICES)
    images = models.ManyToManyField(Images, blank=True)
    url = models.URLField(blank=True, null=True)


class ProjectMaterial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)

    @property_
    def display_cost(self):
        return money_fmt(self.cost, places=4, curr='$')

    @property_
    def display_total_cost(self):
        return money_fmt(self.cost * self.quantity, places=4, curr='$')

    @property_
    def total_cost(self):
        return self.cost * self.quantity
