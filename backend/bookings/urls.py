from django.urls import path
from . import views

urlpatterns = [
    path('inquiries/', views.create_inquiry, name='create-inquiry'),
    path('my-inquiries/', views.my_inquiries, name='my-inquiries'),
    path('owner-inquiries/', views.owner_inquiries, name='owner-inquiries'),
    path('inquiries/<int:pk>/status/', views.update_inquiry_status, name='update-inquiry'),
]
