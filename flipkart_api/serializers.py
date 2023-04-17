from rest_framework import serializers
from .models import Product, Rating, Category, UserProfile, SavedProduct
from django.contrib.auth.models import User
from flipkart_app.models import Order
from rest_framework.authtoken.models import Token


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'image', 'phone']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'date_joined', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data): # to hash password
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data) # user and rest all from profile
        Token.objects.create(user=user)
        return user
    

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name', 'product']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'price', 'description']


class ProductFullSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    seller = UserSerializer(many=False)
    
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'price', 'description', 'seller', 'category']


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    product = ProductSerializer(many=False)
    
    class Meta:
        model = Order
        fields = ['id', 'address', 'zipcode', 'city', 'state', 'ordered_date', 'user', 'product']


class RatingSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False)

    class Meta:
        model = Rating
        fields = ['title', 'description', 'rating', 'user']


class SavedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = SavedProduct
        fields = ['id', 'product']