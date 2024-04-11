# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('patient_homepage/predict', views.predict, name='predict'),
    path('doctor_homepage/predict', views.predict, name='predict'),
]
