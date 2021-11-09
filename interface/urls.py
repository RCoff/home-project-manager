from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('p/add', views.Index.as_view(), name='property-add'),
    path('p/<uuid:id>', views.PropertyView.as_view(), name='property'),
    path('p/<uuid:id>/s/add', views.AddSpaceView.as_view(), name='space-add'),
    path('s/<uuid:id>', views.SpaceView.as_view(), name='space'),
]
