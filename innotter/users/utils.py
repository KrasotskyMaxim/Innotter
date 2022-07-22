import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class UserRegistrationUtils:
    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return make_password(value)
    
class UserLoginUtils(serializers.Serializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get("email")
        password = validated_data.get("password")
        try:
            user = User.objects.get(email=email)
            if not user.password == password:
                raise serializers.ValidationError('Incorrect password!')
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exists!")
        
        return validated_data
    
    def create(self, validated_data):
        return "Login succesful!"