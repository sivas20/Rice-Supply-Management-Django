# from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from .forms import CustomUserCreationForm
# from django.contrib.auth.forms import AuthenticationForm



# # Create your views here.

# def register_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request,'auth/register.html',{'form':form})

# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request,data = request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request,user)
#             return role_based_redirect(user)
#         else:
#             messages.error(request,"Invalid username of password")
#     else:
#         form = AuthenticationForm()
#     return render(request,'auth/login.html',{'form':form})

# def logout_view(request):
#     logout(request)
#     return redirect('login')


# def check_admin(user):
#     return user.is_authenticated and user.role == 'admin'
# def check_manager(user):
#     return user.is_authenticated and user.role == 'manager'
# def check_customer(user):
#     return user.is_authenticated and user.role == 'customer'
# def check_dealer(user):
#     return user.is_authenticated and user.role == 'dealer'

# @login_required(login_url='login')
# @user_passes_test(check_admin)
# def admin_dashboard(request):
#     return render(request, 'RSCMS_app/dashboard.html',{'role':'admin'})

# @login_required(login_url='login')
# @user_passes_test(check_manager)
# def manager_dashboard(request):
#     return render(request, 'RSCMS_app/dashboard.html',{'role':'manager'})

# @login_required(login_url='login')
# @user_passes_test(check_dealer)
# def dealer_dashboard(request):
#     return render(request, 'RSCMS_app/dashboard.html',{'role':'dealer'})

# @login_required(login_url='login')
# @user_passes_test(check_customer)
# def customer_dashboard(request):
#     return render(request, 'RSCMS_app/dashboard.html',{'role':'customer'})

# def role_based_redirect(user):
#     if user.role == 'admin':
#         return redirect('admin_dashboard')
#     elif user.role == 'manager':
#         return redirect('manager_dashboard')
#     elif user.role == 'dealer':
#        return redirect('dealer_dashboard')
#     elif user.role == 'customer':
#        return redirect('customer_dashboard')


from django.shortcuts import render


def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def services(request):
    return render(request, 'services.html')
def project_proposal(request):
    return render(request,"project_proposal.html")