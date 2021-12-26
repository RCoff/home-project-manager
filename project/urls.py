from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id_>', views.ProjectView.as_view(), name='project'),
    path('<uuid:id_>/a/add', views.CreateActionItem.as_view(), name='action-item-add'),
    path('<uuid:id_>/m/add', views.AddMaterialView.as_view(), name='materials-add'),
]