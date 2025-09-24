from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Remove admin role and use radio buttons
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('customer', 'Customer'),
        ('dealer', 'Dealer'),
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Select Role",
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # Override password2 to remove it completely
    password2 = None
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile:
            raise ValidationError("Mobile number is required for OTP verification.")
        
        # Clean the phone number
        mobile = re.sub(r'[^\d+]', '', mobile)
        
        # Validate phone number format
        if len(mobile) < 10:
            raise ValidationError("Please enter a valid mobile number.")
        
        # Check if phone number already exists
        if CustomUser.objects.filter(mobile=mobile).exists():
            raise ValidationError("A user with this mobile number already exists.")
        
        return mobile

    class Meta:
        model = CustomUser
        fields = ['username', 'mobile', 'role', 'password1']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
        }
        labels = {
            'mobile': 'Mobile Number',
            'password1': 'Password'
        }
        help_texts = {
            'mobile': 'This will be used for OTP verification during purchases',
            'password1': 'Choose a strong password'
        }