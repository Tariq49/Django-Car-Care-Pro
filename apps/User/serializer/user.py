from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=False) 

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'date_joined', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
       

    def validate_username(self, value):
        # Check if we are updating an existing user and not changing the username
        if self.instance and value != self.instance.username:
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        password=validated_data.get('password') 
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=password
        )
        return user
    
    
    def update(self, instance, validated_data):
        
        user = instance
        user.username = validated_data.get('username', user.username)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        
        password = validated_data.get('password', None)
        
        if password:
            user.set_password(password)
        
        user.save()
        return instance
