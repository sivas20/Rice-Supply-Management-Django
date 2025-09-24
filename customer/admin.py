from django.contrib import admin
from .models import CustomerProfile
# Register your models here.

class CusmerProfileModel(admin.ModelAdmin):
    list_display = ['full_name','email','get_mobile','address','date_of_birth']
    list_filter = ['created_at', 'date_of_birth']
    search_fields = ['full_name', 'email', 'user__username', 'user__mobile']
    
    def get_mobile(self, obj):
        return obj.user.mobile if obj.user.mobile else 'Not provided'
    get_mobile.short_description = 'Mobile Number'
    
admin.site.register(CustomerProfile,CusmerProfileModel)
