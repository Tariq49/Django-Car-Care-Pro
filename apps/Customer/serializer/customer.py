
from rest_framework import serializers
from django.core.validators import RegexValidator
from apps.Customer.models import Customer
from django.contrib.auth.models import User

class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


    contact_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be exactly 9 digits.")]
    )

    def validate_gender(self, value):
        """Validate that the gender is either 'M' or 'F'."""
        if value not in dict(Customer._meta.get_field('gender').choices):
            raise serializers.ValidationError("Invalid gender choice.")
        return value
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        return super().update(instance, validated_data)
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user']



