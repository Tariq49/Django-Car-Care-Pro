from django.db import models
from django.core.validators import RegexValidator, MinValueValidator 
from django.utils import timezone
from multiselectfield import MultiSelectField

class Specialization(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    

class Mechanic(models.Model):

    DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ]

    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, default=1)
    years_of_experience = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    preferred_job_types = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Freelance', 'Freelance')])
    address = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    work_days = MultiSelectField(choices=DAYS_OF_WEEK , null=True, blank=True, max_choices=7, max_length=50, help_text="Select multiple days using Ctrl or Cmd key")
    

    
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.years_of_experience} years exp"

    class Meta:
        verbose_name_plural = 'Mechanic'
        


