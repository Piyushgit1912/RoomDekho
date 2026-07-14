from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from properties.models import Property


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
