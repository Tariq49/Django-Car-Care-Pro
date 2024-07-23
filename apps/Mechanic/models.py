from django.db import models
from django.core.validators import RegexValidator, MinValueValidator 


# Create your models here.
class Mechanic(models.Model):
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_pic= models.ImageField(upload_to='profile_pic/MechanicProfilePic/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    skill = models.CharField(max_length=500,null=True)
    salary=models.PositiveIntegerField(null=True)
    status=models.BooleanField(default=False)
    years_of_experience = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
  
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


    class Meta:
        verbose_name_plural = 'Mechanic Profile'


