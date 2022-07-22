from rest_framework import serializers

from users.models import User
from users.utils import UserRegistrationUtils, UserLoginUtils

    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "title", "email", "role", "is_blocked")

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "title", "email", "role", "image_s3_path", "is_blocked")
        

class UserRegistrationSerializer(serializers.ModelSerializer, UserRegistrationUtils):
    class Meta:
        model = User
        fields = ("username", "title", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}
        

class UserLoginSerializer(UserLoginUtils):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)  
    