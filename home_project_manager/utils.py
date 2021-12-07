import logging
import uuid

from django.core.exceptions import PermissionDenied

from data.models import Properties, PropertySpaces, PropertyItems, Tasks
from project.models import Projects, ProjectAttachments, ProjectActionItem

logger = logging.getLogger(__name__)


def get_space(space_id: uuid.uuid4):
    return PropertySpaces.objects.get(id=space_id)


def get_property(property_id: uuid.uuid4):
    return Properties.objects.get(id=property_id)


def get_project(project_id: uuid.uuid4):
    return Projects.objects.get(id=project_id)


def get_task(task_id: uuid.uuid4):
    return Tasks.objects.get(id=task_id)


def check_access(request, model_object):
    if request.user not in model_object.users.all():
        raise PermissionDenied


def get_parent_object(id: uuid.uuid4):
    try:
        parent = Properties.objects.get(id=id)
    except Properties.DoesNotExist:
        parent = PropertySpaces.objects.get(id=id)
    return parent
