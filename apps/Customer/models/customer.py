from django.db import models
from django.core.validators import RegexValidator 


class Customer(models.Model):
    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    address = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Customer'
        db_table = "customer"

        constraints = [
           
            models.UniqueConstraint(fields=['contact_number'], name='unique_contact_number'),
              
        ]

        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
       
        full_name = f'{self.user.first_name} {self.user.last_name}'
        return full_name.strip()  
    

    