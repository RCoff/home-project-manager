from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('h/add', views.Index.as_view(), name='property-add'),
    path('h/<uuid:id>', views.PropertyView.as_view(), name='property'),
    path('h/<uuid:id>/s/add', views.AddSpaceView.as_view(), name='space-add'),
    path('s/<uuid:id>', views.SpaceView.as_view(), name='space'),
    path('<uuid:id>/p/add', views.CreateProjectView.as_view(), name='project-add'),
    path('<uuid:id>/t/add', views.CreateTaskView.as_view(), name='task-add'),
    path('p/<uuid:id>', views.ProjectView.as_view(), name='project'),
    path('p/<uuid:id>/a/add', views.CreateActionItem.as_view(), name='action-item-add'),
    path('t/<uuid:id>', views.TaskView.as_view(), name='task'),
]
