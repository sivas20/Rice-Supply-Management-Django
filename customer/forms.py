from django import forms

from .models import CustomerProfile, Purchase_Rice, Payment_For_Rice, DeliveryCostSettings

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'phone_number','Transaction_password', 'address', 'image', 'date_of_birth']
        widgets = {
        'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        'Transaction_password': forms.TextInput(attrs={'class': 'form-control'}),
        'address': forms.Textarea(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PaymentForRiceForm(forms.ModelForm):
    class Meta:
        model = Payment_For_Rice
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PurchaseRiceForm(forms.ModelForm):
    class Meta:
        model = Purchase_Rice
        fields = ['quantity_purchased']
        widgets = {
            'quantity_purchased': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.1',
                'step': '0.1',
                'placeholder': 'Enter quantity in kg'
            }),
        }

class DeliveryCostSettingsForm(forms.ModelForm):
    class Meta:
        model = DeliveryCostSettings
        fields = ['base_cost', 'cost_per_kg', 'max_delivery_cost', 'is_active']
        widgets = {
            'base_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Base delivery cost'
            }),
            'cost_per_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Cost per kg'
            }),
            'max_delivery_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Maximum delivery cost'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'base_cost': 'Base Delivery Cost (৳)',
            'cost_per_kg': 'Cost Per Kg (৳)',
            'max_delivery_cost': 'Maximum Delivery Cost (৳)',
            'is_active': 'Enable These Settings'
        }