from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .forms import AdminProfileForm
from accounts.models import CustomUser
from customer.models import DeliveryCostSettings
from customer.forms import DeliveryCostSettingsForm

# Check if user is an admin
def check_admin(user):
    return user.is_authenticated and user.role == 'admin'

def admin_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check if user is admin
            if user.role == 'admin':
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Admin privileges required.")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'admin/auth/admin_login.html', {'form': form})

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
@user_passes_test(check_admin)
def admin_dashboard(request):
    # Get statistics for dashboard
    from dealer.models import DealerProfile
    from manager.models import ManagerProfile
    from customer.models import CustomerProfile
    
    stats = {
        'total_dealers': DealerProfile.objects.count(),
        'total_managers': ManagerProfile.objects.count(),
        'total_customers': CustomerProfile.objects.count(),
    }
    
    return render(request, 'admin/dashboard.html', {'role': 'admin', 'stats': stats})

@login_required(login_url='admin_login')
@user_passes_test(check_admin)
def delivery_cost_settings(request):
    """Admin view to manage delivery cost settings"""
    settings = DeliveryCostSettings.get_active_settings()
    
    if request.method == 'POST':
        form = DeliveryCostSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery cost settings updated successfully!')
            return redirect('delivery_cost_settings')
    else:
        form = DeliveryCostSettingsForm(instance=settings)
    
    return render(request, 'admin/delivery_cost_settings.html', {
        'form': form,
        'settings': settings
    })
