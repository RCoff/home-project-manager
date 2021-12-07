from django.urls import path
from . import views

urlpatterns = [
    path('p/<uuid:id>', views.ProjectView.as_view(), name='project'),
    path('p/<uuid:id>/a/add', views.CreateActionItem.as_view(), name='action-item-add'),
]