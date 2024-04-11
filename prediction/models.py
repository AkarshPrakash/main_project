from django.db import models

# Create your models here.
# models.py
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='cancer/')
