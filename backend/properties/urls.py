from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
