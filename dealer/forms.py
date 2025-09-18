from django import forms
from .models import DealerProfile, Marketplace, PaddyPurchaseFromFarmer, PaddyStock
from django.core.exceptions import ValidationError

class DealerProfileForm(forms.ModelForm):
     class Meta:
        model = DealerProfile
        exclude = ['user'] 



class PaddyStockForm(forms.ModelForm):
    class Meta:
        model = PaddyStock
        exclude = ['dealer', 'stored_since']  # Dealer set in view
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'moisture_content': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'price_per_something': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_mon': forms.NumberInput(attrs={'class': 'form-control'}),  
            # corrected
            'quality_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }
        
        
        
from django import forms
from .models import DealerProfile, CustomUser

class DealerProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = DealerProfile
        fields = [
            'first_name', 'last_name', 'email',# from User
            'license_number', 'storage_capacity',
            'district', 'upazila', 'union', 'address' # from DealerProfile
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        dealer = super().save(commit=False)
        if commit:
            dealer.user.first_name = self.cleaned_data['first_name']
            dealer.user.last_name = self.cleaned_data['last_name']
            dealer.user.email = self.cleaned_data['email']
            dealer.user.save()
            dealer.save()
        return dealer
    
    
# --- Purchase Form ---
# forms.py
from django import forms
from django.core.validators import MinValueValidator
from .models import PaddyPurchaseFromFarmer

class PaddyPurchaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Enter {self.fields[field].label.lower()}'
            })
        
        # Specific field customizations
        self.fields['farmer_phone'].widget.attrs.update({
            'pattern': '01[3-9]{1}[0-9]{8}',
            'title': 'Please enter a valid Bangladeshi mobile number'
        })
        self.fields['quantity'].widget.attrs.update({
            'min': '0.1',
            'step': '0.1'
        })
        self.fields['purchase_price_per_mon'].widget.attrs.update({
            'min': '0',
            'step': '10'
        })

    class Meta:
        model = PaddyPurchaseFromFarmer
        fields = [
            'farmer_name', 'farmer_phone', 'paddy_type', 'quantity',
            'purchase_price_per_mon', 'moisture_content',
            'transport_cost', 'other_costs', 'notes'
        ]
        widgets = {
            'paddy_type': forms.Select(choices=[
                ('BRRI 28', 'BRRI Dhan 28'),
                ('BRRI 29', 'BRRI Dhan 29'),
                ('BRRI 84', 'BRRI Dhan 84'),
                ('Hybrid', 'Hybrid Variety'),
                ('Local', 'Local Variety'),
            ]),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'purchase_price_per_mon': 'Price per Mon',
            'moisture_content': 'Moisture Content'
        }
        help_texts = {
            'moisture_content': 'Measure with moisture meter (12-14% ideal)',
            'farmer_phone': 'For future communication'
        }

    def clean_moisture_content(self):
        moisture = self.cleaned_data['moisture_content']
        if not 5 <= moisture <= 25:
            raise forms.ValidationError("Moisture content must be between 5% and 25%")
        return round(moisture, 1)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0.1:
            raise forms.ValidationError("Minimum purchase quantity is 0.1 Mon (4kg)")
        return quantity

    def clean_farmer_phone(self):
        phone = self.cleaned_data['farmer_phone']
        if phone and (len(phone) != 11 or not phone.startswith('01')):
            raise forms.ValidationError("Please enter a valid Bangladeshi mobile number")
        return phone 



        
class MarketplaceForm(forms.ModelForm):
    class Meta:
        model = Marketplace
        fields = [
            'paddy_stock', 'name', 'image',
            'quantity', 'moisture_content',
            'price_per_mon', 'quality_notes','status'
        ]
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)