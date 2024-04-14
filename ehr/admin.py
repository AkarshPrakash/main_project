from django.contrib import admin

# Register your models here.
from . models import Patient,Doctor,Appointment,EHR,ApprovalRequest
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(EHR)
admin.site.register(ApprovalRequest)