# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from dealer.forms import DealerProfileForm
from .forms import CustomUserCreationForm
from customer.models import CustomerProfile

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        dealer_form = DealerProfileForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            
            # Ensure mobile is properly set for OTP functionality
            if user.mobile:
                # Clean and format mobile (remove any non-digit characters except +)
                import re
                mobile = re.sub(r'[^\d+]', '', user.mobile)
                if not mobile.startswith('+'):
                    # Add country code if not present (example: +91 for India or +880 for Bangladesh)
                    mobile = mobile.lstrip('0')
                    mobile = '+91' + mobile  # adjust as needed
                user.mobile = mobile
            
            user.save()  # Save user with formatted mobile
            
            # Only save dealer form if the user is a 'dealer'
            if user.role == 'dealer' and dealer_form.is_valid():
                dealer_profile = dealer_form.save(commit=False)
                dealer_profile.user = user  # Link the dealer profile to the created user
                dealer_profile.save()    
            # Auto-create customer profile for customers with basic info
            if user.role == 'customer':
                customer_profile, created = CustomerProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'full_name': user.username,  # Use username as default full name
                        'email': user.email if user.email else '',  # Use email if available
                        'address': 'Please update your address',  # Default address
                    }
                )
            
            messages.success(request, f"Account created successfully! You can now login with your username: {user.username}")
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
        dealer_form=DealerProfileForm()

    return render(request, 'accounts/auth/register.html', {'form': form,"dealer_form":dealer_form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return role_based_redirect(user)
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# Redirect Logic
def role_based_redirect(user):
    if user.role == 'admin':
        # Redirect admin users to admin panel login
        return redirect('admin_login')
    elif user.role == 'manager':
        return redirect('manager_dashboard')
    elif user.role == 'dealer':
        return redirect('dealer_dashboard')
    elif user.role == 'customer':
        return redirect('explore_rice_post')