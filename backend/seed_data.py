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
        'title': 'Cozy Single Room near IIT Delhi',
        'city': 'Delhi', 'location': 'Hauz Khas',
        'price': 7500, 'room_type': 'single',
        'furnished_status': 'furnished', 'gender_preference': 'male',
        'wifi': True, 'security': True, 'status': 'approved',
        'description': 'Well-furnished single room with attached bathroom, 10 min walk from IIT Delhi metro. Hot water, 24x7 security, fast WiFi included.',
    },
    {
        'title': 'Premium PG for Girls near Koramangala',
        'city': 'Bangalore', 'location': 'Koramangala 5th Block',
        'price': 9000, 'room_type': 'pg',
        'furnished_status': 'furnished', 'gender_preference': 'female',
        'wifi': True, 'food': True, 'security': True, 'status': 'approved',
        'description': 'Premium PG with homely food (3 meals), high-speed WiFi, and 24x7 CCTV security. Walking distance from top IT companies.',
    },
    {
        'title': '1 BHK Flat for Rent in Baner',
