from django.db import models
from django.core.validators import MinValueValidator

class MechanicPricePerService(models.Model):
    service_name = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


    def __str__(self):
        return f"{self.service_name} - {self.hourly_rate}"
    

    class Meta:
        verbose_name = "Mechanic Price Per Service"