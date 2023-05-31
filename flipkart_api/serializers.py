from rest_framework import serializers
from .models import Product, Rating, Category, UserProfile, SavedProduct
from django.contrib.auth.models import User
from flipkart_app.models import Order
from rest_framework.authtoken.models import Token
from django.utils import timezone

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'image', 'phone']


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    # profile = UserProfileSerializer()
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'date_joined', 'days_since_joined']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data): # to hash password
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data) # user and rest all from profile
        Token.objects.create(user=user)
        return user
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password!= password2:
            raise serializers.ValidationError('Passwords do not match')
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        
        return account
    
    def get_days_since_joined(self, object):
        return (timezone.now() -object.date_joined).days


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name', 'product']


class ProductSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'price', 'description', 'len_name']
        
    def get_len_name(self, object): # get_nameoffield
        return len(object.name)
        

class ProductFullSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    seller = UserSerializer(many=False)
    
    # if we need only specific attributes
    # category = serializers.StringRelatedField(many=True, read_only=True) # for string fields
    # category = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # for primary key fields
    # category = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='nameinurl') # for url fields
    # we should add context={'request':request} in serializer object in views
    
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'price', 'description', 'seller', 'category']
                

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError('Old and New Passwords cannot be the same')
        return data    


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
        
# Study

# 3.validators
def name_length(value):
    if len(value) < 4:
        raise serializers.ValidationError('Name is too short')
     
     
class ProductTempSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) # core argument read_only, wrie_only, required
    name = serializers.CharField(validators=[name_length]) # validators
    description = serializers.CharField()
    price = serializers.IntegerField()
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def create(self, instance, validated_data): # instance carries old values & validated data carries new values new values
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    
    # 1.field level validation
    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError('Product already exists')
        return value
        
    # 2.object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Title and description cannot be the same')
        return data    

