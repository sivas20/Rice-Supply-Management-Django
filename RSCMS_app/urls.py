from django.contrib import admin
from django.urls import path, include
from RSCMS_app import views


urlpatterns = [    
    path("",views.home, name="home"),   
    path("about/",views.about, name="about"),   
    path("project_proposal/",views.project_proposal, name="project_proposal"),   
    path("services/",views.services, name="services"),   
    path('accounts/', include('accounts.urls')),
    path('dealer/', include('dealer.urls')),
    path('manager/', include('manager.urls')),
    path('customer/', include('customer.urls')),
    path('admin_panel/', include('admin_panel.urls')),
]