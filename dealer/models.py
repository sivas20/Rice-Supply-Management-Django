from django.utils import timezone
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
# Create your models here.

MOISTURE_CATEGORIES = [
    ('Easy', 'Easy (≤13.5%)'),
    ('Medium', 'Medium (13.6%–15.5%)'),
    ('Hard', 'Hard (>15.5%)'),
]

class Location(models.Model):
    """For tracking geographical locations of all parties"""
    district = models.CharField(max_length=50,blank=True,null=True)
    upazila = models.CharField(max_length=50,blank=True,null=True)
    union = models.CharField(max_length=50, blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    class Meta:
        abstract = True  # <-- Make it abstract so no separate table is created

class DealerProfile(Location):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    storage_capacity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.user.username}"
    
    
    
     
# class MillProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # mill_name = models.CharField(max_length=100)
#     # license_number = models.CharField(max_length=50)
    



class PaddyStock(models.Model):
    dealer = models.ForeignKey(DealerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    moisture_category = models.CharField(max_length=10, choices=MOISTURE_CATEGORIES,default='Medium')
    quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    average_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    average_other_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    moisture_content = models.DecimalField(max_digits=4, decimal_places=1)
    image = models.ImageField(upload_to='paddy_images/', blank=True, null=True)
    #this avg price per mon( with transport, other cost)
    price_per_mon = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    stored_since = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    quality_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-last_updated']
        unique_together = ['dealer', 'name', 'moisture_category']

    def __str__(self):
        return f"{self.name} [{self.moisture_category}] - {self.available_quantity} mon"



class PaddyPurchaseFromFarmer(models.Model):
    dealer = models.ForeignKey(DealerProfile, on_delete=models.CASCADE)
    paddy_stock = models.ForeignKey(PaddyStock, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    farmer_name = models.CharField(max_length=100)
    farmer_phone = models.CharField(max_length=15, blank=True)
    paddy_type = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    purchase_price_per_mon = models.DecimalField(max_digits=10, decimal_places=2)
    moisture_content = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(5), MaxValueValidator(25)])
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    # purchase_date = models.DateField(auto_now_add=True)
    reference_code = models.CharField(max_length=20, unique=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-purchase_date']

    def save(self, *args, **kwargs):
        if not self.reference_code:
            count = PaddyPurchaseFromFarmer.objects.count()
            self.reference_code = f"PUR-{timezone.now().year}-{count + 1:04d}"
        
        self.total_cost = (self.quantity * self.purchase_price_per_mon) + self.transport_cost + self.other_costs
        super().save(*args, **kwargs)
        self._sync_stock()

    def _get_moisture_category(self):
        if self.moisture_content <= 13.5:
            return 'Easy'
        elif self.moisture_content <= 15.5:
            return 'Medium'
        return 'Hard'

    def _sync_stock(self):
        category = self._get_moisture_category()
        stock, created = PaddyStock.objects.get_or_create(
            dealer=self.dealer,
            name=self.paddy_type,
            moisture_category=category,
            defaults={
                'moisture_content': self.moisture_content,
                'quantity': 0,
                'available_quantity': 0,
            }
        )
        prev_qty = stock.quantity
        stock.quantity += self.quantity
        stock.available_quantity += self.quantity

        if prev_qty > 0:
            total_qty = stock.quantity

            # Weighted average purchase price
            stock.average_purchase_price = (
                (stock.average_purchase_price * prev_qty + self.purchase_price_per_mon * self.quantity) / total_qty
            )

            # Weighted average transport cost per mon
            new_transport_cost_per_mon = self.transport_cost / self.quantity
            stock.average_transport_cost = (
                (stock.average_transport_cost * prev_qty + new_transport_cost_per_mon * self.quantity) / total_qty
            )

            # ✅ Weighted average of other_costs per mon
            new_other_cost_per_mon = self.other_costs / self.quantity
            stock.average_other_cost = (
                (stock.average_other_cost * prev_qty + new_other_cost_per_mon * self.quantity) / total_qty
            )
        else:
            stock.average_purchase_price = self.purchase_price_per_mon
            stock.average_transport_cost = self.transport_cost / self.quantity
            stock.average_other_cost = self.other_costs / self.quantity

        # ✅ Final price per mon
        stock.price_per_mon = (
            stock.average_purchase_price +
            stock.average_transport_cost +
            stock.average_other_cost
        )

        stock.save()
        self.paddy_stock = stock
        super().save(update_fields=['paddy_stock'])
        
        
        
        
        
        
        
class Marketplace(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Sold', 'Sold'),
    ]

    # সম্পর্কিত স্টক
    paddy_stock = models.ForeignKey(PaddyStock, on_delete=models.CASCADE, related_name='marketplace_posts')
    dealer = models.ForeignKey(DealerProfile, on_delete=models.CASCADE)

    # স্টক থেকে কপি হওয়া ফিল্ড — ফর্মে অটো-ফিল হবে
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='marketplace_images/')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    moisture_content = models.DecimalField(max_digits=4, decimal_places=1)
    price_per_mon = models.DecimalField(max_digits=10, decimal_places=2)
    quality_notes = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    # অতিরিক্ত
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Draft')
    stored_since = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.quantity} mon @ {self.price_per_mon}/mon"

    def save(self, *args, **kwargs):
        if not self.pk:
            # প্রথমবার সেভ হলে প্যাডি স্টক থেকে ডেটা নিয়ে আসা
            self.name = self.name or self.paddy_stock.name
            self.image = self.image or self.paddy_stock.image
            self.moisture_content = self.moisture_content or self.paddy_stock.moisture_content
            self.price_per_mon = self.price_per_mon or self.paddy_stock.price_per_mon
            self.quality_notes = self.quality_notes or self.paddy_stock.quality_notes

            # 🔴 নিরাপত্তা: স্টকে পর্যাপ্ত পরিমাণ আছে কি না
            if self.quantity > self.paddy_stock.available_quantity:
                raise ValueError("Cannot list more than available quantity in stock")

            # 🟡 স্টক থেকে quantity কমানো
            self.paddy_stock.available_quantity -= self.quantity
            self.paddy_stock.save()

        super().save(*args, **kwargs)