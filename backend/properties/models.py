# pyrefly: ignore [missing-import]
from django.db import models
from users.models import CustomUser


class Property(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Sharing'),
        ('triple', 'Triple Sharing'),
        ('flat_1bhk', '1 BHK Flat'),
        ('flat_2bhk', '2 BHK Flat'),
        ('flat_3bhk', '3 BHK Flat'),
        ('pg', 'PG'),
        ('hostel', 'Hostel'),
