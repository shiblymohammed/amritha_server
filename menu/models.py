# _file: dining_project/menu/models.py_
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    
    def __str__(self):
        return self.name

class DailySpecial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)
    date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} on {self.date} ({status})"