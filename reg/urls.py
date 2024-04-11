from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('', views.index,name="index"),
    path('register', views.register,name="register"),
    path('login', views.loginn,name="login"),
    path('index',views.home,name="index"),
    
]