"""tickets URL Configuration"""
from django.contrib import admin
from django.urls import path

from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_tickets/', views.all_tickets),
]
