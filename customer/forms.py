from django import forms
from .models import CustomerProfile, Purchase_Rice, Payment_For_Rice, DeliveryCostSettings
from accounts.models import CustomUser

class CustomerProfileForm(forms.ModelForm):
    mobile = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number (e.g., 01712345678)'
        }),
        help_text="This will be used for OTP verification during purchases"
    )
    
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'email', 'mobile', 'Transaction_password', 'address', 'image', 'date_of_birth']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Transaction_password': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'mobile': 'Mobile Number',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for mobile from the related user
        if self.instance and self.instance.user:
            self.fields['mobile'].initial = self.instance.user.mobile
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile:
            # Clean the phone number
            import re
            mobile = re.sub(r'[^\d+]', '', mobile)
            
            # Validate phone number format
            if len(mobile) < 10:
                raise forms.ValidationError("Please enter a valid mobile number.")
            
            # Check if phone number already exists for other users
            existing_user = CustomUser.objects.filter(mobile=mobile).exclude(id=self.instance.user.id)
            if existing_user.exists():
                raise forms.ValidationError("A user with this mobile number already exists.")
        
        return mobile
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Update the related user's phone number
            if instance.user and self.cleaned_data.get('mobile'):
                import re
                mobile = self.cleaned_data['mobile']
                mobile = re.sub(r'[^\d+]', '', mobile)
                if not mobile.startswith('+'):
                    if not mobile.startswith('880'):
                        mobile = '880' + mobile.lstrip('0')
                    mobile = '+' + mobile
                instance.user.mobile = mobile
                instance.user.save()
        return instance

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