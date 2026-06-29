from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('tenant', 'Tenant'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
