from django.contrib import admin
from django.urls import path, include
from .views import register

urlpatterns = [
    path('', include('django.contrib.auth.urls')),  # For login, logout, password management
    path('register/', register, name='register'),  # For registration
]