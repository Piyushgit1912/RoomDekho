from django.urls import path
from . import views

urlpatterns = [
    path('properties/<int:property_id>/reviews/', views.reviews, name='reviews'),
    path('reviews/<int:pk>/', views.delete_review, name='delete-review'),
]
