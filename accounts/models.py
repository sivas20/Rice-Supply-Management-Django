from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
        ('dealer', 'Dealer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    mobile = models.CharField(max_length=20, blank=True, null=True, help_text="Mobile number for OTP verification")
    
    def __str__(self):
        return self.username