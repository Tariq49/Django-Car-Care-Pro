from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.Mechanic.models import Mechanic,Specialization
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = [ 'name']
        

class MechanicSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    work_days = serializers.MultipleChoiceField(choices=Mechanic.DAYS_OF_WEEK, allow_empty=True)
    

    specializations = serializers.ListField(child=serializers.CharField(), write_only=True)
   
    contact_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be exactly 9 digits.")]
    )
    
    class Meta:
        model = Mechanic
        fields = [
            'id', 'user', 'specializations', 'years_of_experience', 
            'preferred_job_types', 'address', 'gender', 'contact_number', 
            'profile_image', 'work_days'
        ]
    
    def get_specializations_display(self, obj):
        """Return a list of specialization names for the mechanic."""
        return [spec.name for spec in obj.specializations.all()]

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
        
        specializations_texts = validated_data.pop('specializations', [])

        # Create the Mechanic instance
        mechanic = Mechanic.objects.create(**validated_data)

        # Handle specializations
        specializations = [Specialization.objects.get_or_create(name=text)[0] for text in specializations_texts]
        mechanic.specializations.set(specializations)

        return mechanic


    def update(self, instance, validated_data):
        # Extract and update specializations if provided
        specializations_texts = validated_data.pop('specializations', None)
        if specializations_texts is not None:
            # Convert names to Specialization instances
            specializations = []
            for text in specializations_texts:
                specialization, created = Specialization.objects.get_or_create(name=text)
                specializations.append(specialization)
            instance.specializations.set(specializations)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


