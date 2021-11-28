from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

property_ = property


class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField()


class Tasks(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    description = models.TextField()
    start_datetime = models.DateTimeField(null=False, blank=False, default=now)
    end_datetime = models.DateTimeField(null=True, blank=True)
    images = models.ManyToManyField(Images, blank=True)


class Properties(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, blank=False)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=140, null=True, blank=True)
    city = models.CharField(max_length=140, null=True, blank=True)
    state = models.CharField(max_length=140, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=True)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    thumbnail = models.ForeignKey(Images, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_property'),
        ]

    def check_users(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.id})"


class PropertySpaces(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Properties, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=140)
    tasks = models.ManyToManyField(Tasks, blank=True)

    def __str__(self):
        return f"{self.property.name} - {self.name} ({self.id})"

    class Meta:
        unique_together = [['property', 'name']]


class PropertyItems(models.Model):
    id = models.OneToOneField(Properties, primary_key=True, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Tasks, blank=True)


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

    def __str__(self):
        if self.property_space:
            return f"{self.property.name} - {self.property_space.name} - {self.name} ({self.id})"
        else:
            return f"{self.property.name} - Home - {self.name} ({self.id})"


class ProjectAttachments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    description = models.TextField()
    images = models.ManyToManyField(Images, blank=True)
