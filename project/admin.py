from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Projects)
admin.site.register(models.ProjectActionItem)
admin.site.register(models.ProjectAttachments)
