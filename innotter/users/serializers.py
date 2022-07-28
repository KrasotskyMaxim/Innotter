import jwt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import make_password

from users.models import User
from innotter.settings import JWT_SECRET
from users.utils import create_jwt_token_dict

    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "title", "email", "role", "image_s3_path", "is_blocked")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "title", "email", "role", "image_s3_path", "is_blocked")
        read_only_fields = ("id", "username", "title", "email", "image_s3_path")

    is_blocked = serializers.BooleanField()
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "title", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
        
    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        return make_password(value)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)  
    access = serializers.CharField(required=False)
    refresh = serializers.CharField(required=False)
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        email = validated_data.get("email")
        password = validated_data.get("password")
        try:
            user = User.objects.get(email=email)
            if not user.password == password:
                raise serializers.ValidationError("Incorrect password!")
            validated_data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exists!")
        
        return validated_data
    
    def create(self, validated_data):
        jwt_token_dict = create_jwt_token_dict(to_refresh=False, validated_data=validated_data)
        
        return jwt_token_dict
        

class UserRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(required=False)
    refresh = serializers.CharField(required=False)
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        refresh_token = validated_data.get("refresh_token")
        try:
            payload = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=["HS256"])
            if payload.get("token_type") != "refresh":
                raise serializers.ValidationError("Token isn't refresh!")
            validated_data["payload"] = payload
        except jwt.ExpiredSignatureError: 
            raise serializers.ValidationError("Refresh token is expired!")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Refresh token isn't valid!")
        
        return validated_data

    def create(self, validated_data):
        jwt_token_dict = create_jwt_token_dict(to_refresh=True, validated_data=validated_data)
        
        return jwt_token_dict
    