
from rest_framework import serializers
from django.core.validators import RegexValidator
from apps.Customer.models import Customer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    customer_name = serializers.SerializerMethodField()

    contact_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be exactly 9 digits.")]
    )
    
    def validate(self, data):
        user = data.get('user')
        if Customer.objects.filter(user=user).exists():
            raise ValidationError({"user": "This user already has a customer record."})
        return data

    def get_customer_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() if obj.user else None

    
    def validate_gender(self, value):
        """Validate that the gender is either 'M' or 'F'."""
        if value not in dict(Customer._meta.get_field('gender').choices):
            raise serializers.ValidationError("Invalid gender choice.")
        return value
    
    def create(self, validated_data):
        user = validated_data.get('user')
        user_id = user.id if isinstance(user, User) else user  
        
        
        if Customer.objects.filter(user=user).exists():
            raise serializers.ValidationError("This user already has a customer record.")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        return super().update(instance, validated_data)
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user', 'customer_name']

