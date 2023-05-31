from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .serializers import (ProductSerializer, UserProfileSerializer, UserSerializer, OrderSerializer, 
                          RatingSerializer, CategorySerializer, ProductFullSerializer, 
                          ChangePasswordSerializer, SavedProductSerializer, ProductTempSerializer)
from .models import Product, Rating, Category, UserProfile, SavedProduct
from flipkart_app.models import Order
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination
from .permission import CustomAdminPermissions
from flipkart_api import signals
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .throttling import ReviewThrottling

# Create your views here.


class ProductsViewset(ModelViewSet):
    """
    Viewset to get, post, update, delete a product
    Get full details while taking detail of particuar product
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    authentication_classes = (TokenAuthentication, )
    # permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        seller = self.request.user
        serializer = ProductFullSerializer(instance, many=False, 
                                           context={'request': request, 'seller': seller})
        return Response(serializer.data)


class ProductView(APIView):
    """
    In GET: Obtain list of all products
    In POST: Creates a new products
    """
    # permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by('id')
        
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(page, many=True) # more than one object so many=True
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            Product.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)


class ProductDetailView(APIView):
    """
    In GET: Obtain a particular product
    In PUT: Updates a particular product
    In DELETE: Deletes a particular product
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        queryset = Product.objects.get(id=id)
        serializer = ProductSerializer(queryset)
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        id = kwargs.get("id")

        # import pdb
        # pdb.set_trace()
        
        queryset = Product.objects.get(id=id)
        serializer = ProductSerializer(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        queryset = Product.objects.get(id=id)
        queryset.delete()
        return Response({"msg": "deleted"})


class ProductSearchFilter(ListAPIView):
    """
    Search product with name and order them by name field
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', ) # ?search=value in url
    ordering_fields = ('rating', ) # ?ordering=attribute in url


class CategoryViewset(ModelViewSet):
    """
    Display category for all products
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )


class UserProfileViewset(ModelViewSet):
    """
    Obtain profile of current user
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )


class UserViewset(ModelViewSet):
    """
    Obtain list of all the main
    Change current password and set new password
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    # permission_classes = (AllowAny, )

    @action(methods=['PUT'], detail=True, serializer_class=ChangePasswordSerializer, permission_classes=[IsAuthenticated])
    def change_password(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'message':'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message':'Password Updated'}, status=status.HTTP_200_OK)


class OrdersViewset(ModelViewSet):
    """
    Obtain list of all the orders by customers
    """
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )


class RatingViewset(ModelViewSet):
    """
    Post the review and get all the reviews
    """
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    # permission_classes = (IsAuthenticated, )
    

class CustomObtainAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key = response.data['token'])
        user = User.objects.get(id = token.user_id)
        serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})
    

class SavedProductView(APIView):
    # permission_classes = (AllowAny, )

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        saved_product = SavedProduct.objects.create(currentuser=request.user, product=product)
        serializer = SavedProductSerializer(saved_product, many=False)
        return Response(serializer.data)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        SavedProduct.objects.filter(currentuser=request.user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedProductViewset(ModelViewSet):

    queryset = SavedProduct.objects.all().order_by('id')
    serializer_class = SavedProductSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
# if we use ReadOnlyModelViewSet, thenonly get method works


# Study 

def product_list_s(request):
    queryset = Product.objects.all()
    data = {
        'Products' : list(queryset.values())
        } # convert queryset to python dictionary
    return JsonResponse(data)


def product_detail_s(request, pk):
    queryset = Product.objects.get(pk=pk)
    data = {
        'Name' : queryset.name,
        'Description' : queryset.description
        }
    return JsonResponse(data)


@api_view(['GET', 'POST'])
def product_list(request):
    
    if request.method == 'GET':
        queryset = Product.objects.all().order_by('id')
        serializer = ProductTempSerializer(queryset, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductTempSerializer(data=request.data)
        if serializer.is_valid():
            Product.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)
 
 
@api_view(['GET', 'PUT', 'DELETE'])  
@permission_classes([IsAuthenticated]) 
def product_detail(request, pk):
    
    if request.method == 'GET':
        try:
            queryset = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductTempSerializer(queryset)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        queryset = Product.objects.get(pk=pk)
        serializer = ProductSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    if request.method == 'DELETE':
        queryset = Product.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)    
    
        
class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Category.objects.filter(product=pk)


class CategoryCreate(generics.CreateAPIView):
    serializer_class = CategorySerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        prod = Product.objects.get(pk=pk)
        serializer.save(product=prod)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


#Filtering
class RatingView(generics.ListAPIView):
    serializer_class = RatingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'user__username']
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewThrottling]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-throttle'
    
    def get_queryset(self):
        username = self.kwargs['username'] # to use 1st url
        # username = self.request.query_params.get('username', None) # to pass ?username=tinu in 2nd url 
        return Rating.objects.filter(user__username=username) # __username is for foriegnkey only to specify attribute
    

@api_view(['POST',])
# @throttle_classes([UserRateThrottle, AnonRateThrottle])
def registration_view(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
    
    
@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)