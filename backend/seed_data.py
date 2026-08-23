"""
Seed sample data into the database.

Usage (from the backend/ folder):
    python manage.py shell < seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roomdekho.settings')
django.setup()

from users.models import CustomUser
from properties.models import Property

# Sample owner
owner, created = CustomUser.objects.get_or_create(
    username='sample_owner',
