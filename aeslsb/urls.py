from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('patient_homepage/aeslsb', views.aeslsb, name='aeslsb'),
    path('doctor_homepage/aeslsb', views.aeslsb, name='aeslsb'),
]
