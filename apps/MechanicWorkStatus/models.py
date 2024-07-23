from django.db import models
from apps.Mechanic.models import Mechanic
from apps.CustomerServiceRequest.models import CustomerServiceRequest 
# Create your models here.
class MechanicWorkStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    service_request = models.ForeignKey(CustomerServiceRequest, on_delete=models.CASCADE)
    date_completed = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(null=True, blank=True)
#mechanic = ForeignKey(Mechanic, on_delete=models.CASCADE)
#service_request = ForeignKey(CustomerServiceRequest
#date_completed 
#status (pending, in progress, completed, cancelled)
#remarks 
