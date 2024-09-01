from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.Mechanic.models import Mechanic,Specialization
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



        

class MechanicSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_full_name = serializers.SerializerMethodField()
    work_days = serializers.MultipleChoiceField(choices=Mechanic.DAYS_OF_WEEK, allow_empty=True)
    

 
   
    contact_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be exactly 9 digits.")]
    )
    
    class Meta:
        model = Mechanic
        fields = [
            'id', 'user','user_full_name', 'years_of_experience', 
            'preferred_job_types', 'address', 'gender', 'contact_number', 
            'profile_image', 'work_days'
        ]
    
    def get_user_full_name(self, obj):
       
        user = obj.user
        if user:
            return f"{user.first_name} {user.last_name}".strip()  # Ensure no extra spaces if any name part is missing
        return None

    def validate_years_of_experience(self, value):
        """Ensure the years of experience is a non-negative integer."""
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        return value

    def validate_preferred_job_types(self, value):
        """Ensure the preferred job type is one of the allowed choices."""
        valid_job_types = dict(Mechanic._meta.get_field('preferred_job_types').choices).keys()
        if value not in valid_job_types:
            raise serializers.ValidationError(f"Invalid job type. Must be one of {', '.join(valid_job_types)}.")
        return value
    
    def validate_gender(self, value):
        """Ensure the gender is one of the allowed choices."""
        valid_genders = dict(Mechanic._meta.get_field('gender').choices).keys()
        if value not in valid_genders:
            raise serializers.ValidationError(f"Invalid gender. Must be one of {', '.join(valid_genders)}.")
        return value

    def validate_work_days(self, value):
        """Ensure work days are valid days of the week."""
        valid_days = dict(Mechanic.DAYS_OF_WEEK).keys()
        for day in value:
            if day not in valid_days:
                raise serializers.ValidationError(f"Invalid work day. Must be one of {', '.join(valid_days)}.")
        return value

    def create(self, validated_data):
     
        user = validated_data.get('user')
        if Mechanic.objects.filter(user=user).exists():
            raise serializers.ValidationError("A mechanic with this user ID already exists.")
        return Mechanic.objects.create(**validated_data)


    def update(self, instance, validated_data):
      
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


