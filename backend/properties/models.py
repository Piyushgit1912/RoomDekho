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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    custom_room_type= models.CharField(max_length=100, blank=True)

    independence_type= models.CharField(max_length=20,
                                        choices=INDEPENDENCE_CHOICES,
                                        default='independent'
                                        )
    
    furnished_status = models.CharField(max_length=15, choices=FURNISHED_CHOICES, default='unfurnished')

    gender_preference = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')

    # Amenities
    wifi = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    ac = models.BooleanField(default=False)
