from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserProfileSerializer, UserSerializer, OrderSerializer, RatingSerializer, CategorySerializer, ProductFullSerializer, ChangePasswordSerializer, SavedProductSerializer
from .models import Product, Rating, Category, UserProfile, SavedProduct
from flipkart_app.models import Order
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 8


class ProductsViewset(ModelViewSet):
    """
    Viewset to get, post, update, delete a product
    Get full details while taking detail of particuar product
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        seller = self.request.user
        serializer = ProductFullSerializer(instance, many=False, context={'request': request, 'seller': seller})
        return Response(serializer.data)


class ProductView(APIView):
    """
    In GET: Obtain list of all products
    In POST: Creates a new products
    """
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by('id')

        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = ProductSerializer(page, many=True)
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
    search_fields = ('name', )


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
    permission_classes = (AllowAny, )

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
    permission_classes = (IsAuthenticatedOrReadOnly, )


class RatingViewset(ModelViewSet):
    """
    Post the review and get all the reviews
    """
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    

class CustomObtainAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key = response.data['token'])
        user = User.objects.get(id = token.user_id)
        serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})
    

class SavedProductView(APIView):
    permission_classes = (AllowAny, )

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
