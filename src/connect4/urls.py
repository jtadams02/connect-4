from django.urls import path,include
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.views.generic import TemplateView
from . import views

def custom_logout(request):
    logout(request)
    return redirect('home')

urlpatterns = [
    path("",views.home, name="home"),
    path("login/",views.oauth_login, name='login'),
    path("logout/",custom_logout,name='logout'),
    path('register',views.register,name='register'),
    path('export/', views.export_results, name='export_results'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    path('profile/', views.user_profile, name='user_profile'),
    path('toggle_visibility/<int:file_id>/', views.toggle_visibility, name='toggle_visibility'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
]
