from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'price', 'description']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(read_only=True)
    password2 = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs

    # def create(self, validated_data):
    #     return User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        
    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']