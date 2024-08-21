# models.py
from django.db import models
from django.contrib.auth.models import User
from apps.core.constants import SERVICE_NEEDED_CHOICES
from apps.Mechanic.models.mechanic import Mechanic 
from django.utils import timezone

class ServiceRequest(models.Model):

    CATEGORY_CHOICES = [
        ('Two_wheeler_with_gear', 'Two_wheeler_with_gear'),
        ('Two_wheeler_without_gear','Two_wheeler_without_gear'),
        ('Four_wheeler', 'Four Wheeler'),
        ('Three_wheeler','Three_wheeler')
    ]
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    vehicle_no = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_brand = models.CharField(max_length=50)
    problem_description = models.TextField()
    date_of_request = models.DateTimeField(default=timezone.now)  
    service_name = models.CharField(max_length=50,choices=SERVICE_NEEDED_CHOICES)
    
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'vehicle_no', 'problem_description','service_name'], name='unique_service_request')
        ]

   
    def __str__(self):
        return f'Service Request {self.vehicle_no} by {self.customer.user.username}'
