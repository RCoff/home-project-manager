from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid

property_ = property


class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(upload_to="uploads/")


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
    zipcode = models.IntegerField(null=True, blank=True, validators=[MaxLengthValidator(5),
                                                                     MinLengthValidator(5)])
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
    thumbnail = models.ForeignKey(Images, on_delete=models.CASCADE, blank=True, null=True)
    tasks = models.ManyToManyField(Tasks, blank=True)

    def __str__(self):
        return f"{self.property.name} - {self.name} ({self.id})"

    class Meta:
        unique_together = [['property', 'name']]


class PropertyItems(models.Model):
    id = models.OneToOneField(Properties, primary_key=True, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Tasks, blank=True)

