from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'status', 'contact_number', 'date']
    list_filter = ['status']
