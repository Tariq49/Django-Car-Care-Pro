from django.db import models
from apps.Mechanic.models import Mechanic
# Create your models here.
class Attendance(models.Model):
    PRESENT_STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]


    mechanic=models.ForeignKey(Mechanic,on_delete=models.CASCADE,null=True)
    date=models.DateField()
    present_status = models.CharField(max_length=10, choices=PRESENT_STATUS_CHOICES, default="present")

    def __str__(self):
        return f"{self.mechanic.username} - {self.date} - {self.present_status}"