from django.db import models
from reg.models import CustomUser
from storages.backends.s3boto3 import S3Boto3Storage

# Patient Model
class Patient(models.Model):
    id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    location = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='patient_profile_pics', null=True, blank=True,storage=S3Boto3Storage())
    user_id = models.CharField(max_length=20, unique=True, null=False, default=1)
    contact_information = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # New email field

    def __str__(self):
        return self.name

# Doctor Model
class Doctor(models.Model):
    id = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    user_id = models.CharField(max_length=20, unique=True, null=False, default=10000)
    name = models.CharField(max_length=100)
    specification = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='doctor_profile_pics', null=True, blank=True,storage=S3Boto3Storage())
    location = models.CharField(max_length=255, null=True, blank=True)  # Location field
    contact_information = models.CharField(max_length=255, null=True, blank=True)  # Contact information field
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)  # New email field

    def __str__(self):
        return self.name


# Appointment Model
class Appointment(models.Model):
    PATIENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    status = models.CharField(max_length=10, choices=PATIENT_STATUS_CHOICES)
    class Meta:
        unique_together = ('doctor', 'patient')

    def __str__(self):
        return f"Appointment for {self.patient.name} with Dr. {self.doctor.name} on {self.date} at {self.time}"
    

class EHR(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)
    last_modified = models.DateTimeField(auto_now=True)
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    personal_history = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    drug_history = models.TextField(blank=True)
    vital_signs = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    xray_image = models.ImageField(upload_to='ehr/xray/', blank=True,storage=S3Boto3Storage())
    lab_result_image = models.ImageField(upload_to='ehr/lab_result/', blank=True,storage=S3Boto3Storage())



class ApprovalRequest(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    record = models.ForeignKey(EHR, on_delete=models.CASCADE,null=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')

    def approve_request(self):
        self.status = 'approved'
        self.save()

    def deny_request(self):
        self.status = 'denied'
        self.save()    
