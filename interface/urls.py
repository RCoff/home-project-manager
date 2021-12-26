from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('h/add', views.AddPropertyView.as_view(), name='property-add'),
    path('h/<uuid:id_>', views.PropertyView.as_view(), name='property'),
    path('h/<uuid:id_>/s/add', views.AddSpaceView.as_view(), name='space-add'),
    path('s/<uuid:id_>', views.SpaceView.as_view(), name='space'),
    path('<uuid:id_>/p/add', views.CreateProjectView.as_view(), name='project-add'),
    path('<uuid:id_>/t/add', views.CreateTaskView.as_view(), name='task-add'),
    path('t/<uuid:id_>', views.TaskView.as_view(), name='task'),
]
