from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('p/<uuid:id>', views.PropertyView.as_view(), name='property'),
    path('p/<uuid:property_id>/<uuid:space_id>', views.SpaceView.as_view(), name='space')
]
