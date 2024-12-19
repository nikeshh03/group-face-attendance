from django.db import models
from datetime import datetime

class Attendance(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'date']