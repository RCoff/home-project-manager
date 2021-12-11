from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>', views.ProjectView.as_view(), name='project'),
    path('<uuid:id>/a/add', views.CreateActionItem.as_view(), name='action-item-add'),
    path('<uuid:id>/m/add', views.AddMaterialView.as_view(), name='materials-add'),
]