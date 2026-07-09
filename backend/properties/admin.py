from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'price', 'room_type', 'status', 'owner', 'created_at']
    list_filter = ['status', 'room_type', 'city', 'furnished_status']
    search_fields = ['title', 'city', 'location', 'owner__name']
    inlines = [PropertyImageInline]
    actions = ['approve_properties', 'reject_properties']

    def approve_properties(self, request, queryset):
