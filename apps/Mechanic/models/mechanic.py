from django.db import models
from django.core.validators import RegexValidator, MinValueValidator 
from django.utils import timezone

class Specialization(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    

class Mechanic(models.Model):
    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, default=1)
    specializations =  models.ManyToManyField(Specialization,related_name='mechanics') 
    years_of_experience = models.PositiveIntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    preferred_job_types = models.CharField(max_length=50, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Freelance', 'Freelance')])
    address = models.TextField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    contact_number = models.CharField(max_length=15,validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be 9 digits.")])
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    work_days = models.CharField(max_length=50) 
    

    

    def get_specializations(self):
        return ", ".join([s.name for s in self.specializations.all()])

    def __str__(self):
        full_name = f"{self.user.first_name} {self.user.last_name}"
        specializations = self.get_specializations()
        return f"{full_name} - {self.years_of_experience} years experience, Specializations: {specializations}"


    class Meta:
        verbose_name_plural = 'Mechanic'


