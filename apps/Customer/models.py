from django.db import models
from django.core.validators import RegexValidator 
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.TextField()
    email = models.EmailField(unique=True,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Customer Profile'