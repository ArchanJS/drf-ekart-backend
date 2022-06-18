from rest_framework import serializers
from .models import User,Product
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

# Serializers

class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)
    class Meta:
        model=User
        fields='__all__'

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

class ProductCreationSerializer(serializers.ModelSerializer):
    postedby = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Product
        fields=['id','productName','description','productPrice','quantity','photo','postedby']

class ProductGetSerializer(serializers.ModelSerializer):
    postedby = UserSerializer(read_only=True)
    class Meta:
        model=Product
        fields='__all__'