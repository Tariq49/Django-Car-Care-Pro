from django.db import models
from django.core.validators import RegexValidator 


class Customer(models.Model):
    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Customer Registrations'
        db_table = "customer"

        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
            models.UniqueConstraint(fields=['contact_number'], name='unique_contact_number'),
            models.UniqueConstraint(fields=['user', 'email'], name='unique_user_email'),
            models.UniqueConstraint(fields=['user', 'first_name', 'last_name'], name='unique_user_first_last_name'),
        ]

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'