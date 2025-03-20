from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from . import views
def custom_logout(request):
    logout(request)
    return redirect('home')
urlpatterns = [
    path("",views.home, name="home"),
    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    path("logout/",custom_logout,name='logout'),
    path('register',views.register,name='register')
]
