
from rest_framework import serializers
from django.core.validators import RegexValidator
from apps.Customer.models import Customer
from .user import UserSerializer

class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer()


    contact_number = serializers.CharField(
        validators=[RegexValidator(regex=r'^\d{9}$', message="Contact number should be exactly 9 digits.")]
    )

    def validate_gender(self, value):
        """Validate that the gender is either 'M' or 'F'."""
        if value not in dict(Customer._meta.get_field('gender').choices):
            raise serializers.ValidationError("Invalid gender choice.")
        return value
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)
        return super().update(instance, validated_data)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['user']



