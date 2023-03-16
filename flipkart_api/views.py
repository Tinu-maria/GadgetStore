from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer, OrderSerializer, RatingSerializer
from .models import Product, Rating
from flipkart_app.models import Order

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 8


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

        import pdb
        pdb.set_trace()
        
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


class ProductsViewset(ModelViewSet):
    """
    Viewset to get, post, update, delete a product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class ProductSearchFilter(ListAPIView):
    """
    Search product with name and order them by any fields
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', )
    

class CustomerView(ModelViewSet):
    """
    Obtain list of all customers profile
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrdersView(ModelViewSet):
    """
    Obtain list of all customers order
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class RatingView(ModelViewSet):
    """
    Get all the reviews of app and post your review
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
        

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer


# class LoginView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request, format=None):
#         serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return Response(None, status=status.HTTP_202_ACCEPTED)
