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
    problem_description = models.TextField()
    date_of_request = models.DateTimeField(default=timezone.now)  
    service_name = models.CharField(max_length=50,choices=SERVICE_NEEDED_CHOICES)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.SET_NULL, null=True)
    mechanic_update = models.TextField(blank=True, null=True)  # Mechanic's updates about the work
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, In Progress, Completed
    completed_date = models.DateTimeField(blank=True, null=True)
                                          
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer',  'problem_description','service_name'], name='unique_service_request')
        ]

   
    def __str__(self):
        mechanic_name = f"Mechanic: {self.mechanic.user.get_full_name()}" if self.mechanic else "No Mechanic Assigned"
        return (f'Service Request: {self.customer.user.username} | '
                f'Service Name: {self.service_name} | '
                f'Problem Description: {self.problem_description} | '
                f'{mechanic_name}')
    
    def save(self, *args, **kwargs):
        # Automatically set the completed date when the status is set to 'Completed'
        if self.status == 'Completed' and self.completed_date is None:
            self.completed_date = timezone.now()
        super(ServiceRequest, self).save(*args, **kwargs)     

class Vehicle(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='vehicles', null=True)
    vehicle_no = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_brand = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.vehicle_brand} {self.vehicle_model} ({self.vehicle_no})'
