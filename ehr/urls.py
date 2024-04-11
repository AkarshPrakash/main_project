from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path( 'doctor_homepage/'  , views.doctor_homepage, name='doctor_homepage'),
    
    path('doctor_homepage/doctor_appointment/', views.doctor_appointment),
    path('doctor_homepage/doctor_profile', views.doctor_profile),
    path('doctor_homepage/doctor_ehr', views.doctor_ehr,name='doctor_ehr' ),
    path('doctor_homepage/doctor_ehr/doctor_edit/<int:patient_id>', views.doctor_edit,name='doctor_edit'),
    path('doctor_homepage/doctor_ehr/doctor_view/<int:patient_id>', views.doctor_view,name='doctor_view'),
    path('doctor_homepage/search_patient/', views.search_patient, name='search_patient'),
    path('patient_homepage/', views.patient_homepage, name='patient_homepage'),
    path('patient_homepage/cancer_detection', views.cancer_detection, name='cancer_detection'),
    path('patient_homepage/patient_appointment', views.patient_appointment, name='patient_appointment'),
    path('patient_homepage/search_doctor', views.search_doctor, name='search_doctor'),
    path('patient_homepage/patient_ehr', views.patient_ehr, name='patient_ehr'),
    path('patient_homepage/patient_ehr/view_ehr', views.view_ehr, name='view_ehr'),
    path('patient_homepage/patient_ehr/edit_ehr', views.edit_ehr, name='edit_ehr'),
    path('patient_homepage/patient_ehr/pending_requests', views.pending_requests, name='pending_requests'),
    path('patient_homepage/patient_profile', views.patient_profile, name='patient_profile'),
    path( 'doctor_homepage/index'  , views.index, name='index'),
    path( 'patient_homepage/index'  , views.index, name='index'),
]