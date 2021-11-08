from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Properties)
admin.site.register(models.PropertyItems)
admin.site.register(models.PropertySpaces)
admin.site.register(models.Projects)
admin.site.register(models.ProjectAttachments)
admin.site.register(models.Tasks)
admin.site.register(models.Images)
