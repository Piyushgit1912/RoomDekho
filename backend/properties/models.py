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
        ('studio', 'Studio Apartment'),
        ('other','Other (Custom)'),
    ]
    INDEPENDENCE_CHOICES=[
        ('independent','Independent'),
        ('non_independent','Non-Independent'), 
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Fully Furnished'),
        ('semi', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Male Only'),
        ('female', 'Female Only'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
