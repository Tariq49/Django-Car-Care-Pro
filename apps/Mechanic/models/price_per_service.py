from django.db import models
from django.core.validators import MinValueValidator
from apps.Mechanic.models import Mechanic
from apps.core.constants import SERVICE_NEEDED_CHOICES
from django.core.exceptions import ValidationError

class MechanicPricePerService(models.Model):

        
    CURRENCY_CHOICES = [
        ('Euro', 'Euro'),
        ('Dollar', 'US Dollar'),
        ('Pound', 'British Pound'),
       
    ]

    
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50,choices=SERVICE_NEEDED_CHOICES)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(100)])
    currency = models.CharField(max_length=6, choices=CURRENCY_CHOICES, default='Euro')

    def __str__(self):
        return f"{self.mechanic.user.first_name}{self.mechanic.user.last_name} - {self.mechanic.years_of_experience} years exp- {self.service_name} - {self.hourly_rate} {self.currency}"

    
    class Meta:
        verbose_name = "Mechanic Price Per Service"
        constraints = [
            models.UniqueConstraint(fields=['mechanic', 'service_name'], name='unique_user_specialization')
        ]