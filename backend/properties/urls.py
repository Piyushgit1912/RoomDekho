from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', views.property_detail, name='property-detail'),
    path('add-property/', views.add_property, name='add-property'),
    path('update-property/<int:pk>/', views.update_property, name='update-property'),
    path('delete-property/<int:pk>/', views.delete_property, name='delete-property'),
    path('my-properties/', views.my_properties, name='my-properties'),
    path('admin/properties/', views.admin_properties, name='admin-properties'),
    path('admin/properties/<int:pk>/approve/', views.admin_approve_property, name='admin-approve'),
]
