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
    laundry = models.BooleanField(default=False)
    food = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    security = models.BooleanField(default=False)

    # Contact
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.EmailField(blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} – {self.city}"

    @property
    def avg_rating(self):
        revs = self.reviews.all()
        if revs.exists():
            return round(sum(r.rating for r in revs) / revs.count(), 1)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image – {self.property.title}"

class PropertyVideo(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    video = models.FileField(upload_to='property_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video - {self.property.title}"