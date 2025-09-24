from django.db import models
from accounts.models import CustomUser
from manager.models import RicePost
from decimal import Decimal
# Create your models here.

class DeliveryCostSettings(models.Model):
    """Admin-configurable delivery cost settings"""
    base_cost = models.DecimalField(max_digits=6, decimal_places=2, default=50.00, 
                                   help_text="Base delivery cost in Taka")
    cost_per_kg = models.DecimalField(max_digits=6, decimal_places=2, default=5.00,
                                     help_text="Additional cost per kg in Taka")
    max_delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=200.00,
                                           help_text="Maximum delivery cost cap in Taka")
    is_active = models.BooleanField(default=True, help_text="Enable/disable these settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Delivery Cost Setting"
        verbose_name_plural = "Delivery Cost Settings"
    
    def __str__(self):
        return f"Delivery Settings - Base: ৳{self.base_cost}, Per kg: ৳{self.cost_per_kg}"
    
    @classmethod
    def get_active_settings(cls):
        """Get the active delivery cost settings"""
        settings = cls.objects.filter(is_active=True).first()
        if not settings:
            # Create default settings if none exist
            settings = cls.objects.create()
        return settings
class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'customer'}, 
        related_name="customerprofile"
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)  # replaced phone_number with email
    Transaction_password = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField()
    image = models.ImageField(upload_to="customer_profile/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.full_name

        
class Purchase_Rice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Cancel', 'Cancel'),
        ('Shipping', 'Shipping'),
        ('Delivered', 'Delivered'),
        ('Successful', 'Successful'),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_rice_purchases')
    rice = models.ForeignKey(RicePost, on_delete=models.CASCADE, related_name='customer_rice_orders')
    quantity_purchased = models.FloatField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_or_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_confirmed = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # ✅ New field
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rice Purchase by {self.customer.username} - {self.rice.rice_name}"
    
    
    
class Payment_For_Rice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_rice_payments')
    rice = models.ForeignKey(RicePost, on_delete=models.CASCADE, related_name='rice_customer_payments')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"