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
    defaults={
        'name': 'Rajesh Kumar',
        'email': 'rajesh@roomdekho.com',
        'user_type': 'owner',
        'phone': '9876543210',
    }
)
if created:
    owner.set_password('password123')
    owner.save()
    print(f"Owner created: username=sample_owner  password=password123")
else:
    print("Owner already exists.")

# Sample properties
samples = [
    {
