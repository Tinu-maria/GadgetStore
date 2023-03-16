from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("productset", views.ProductsViewset, basename="productset")
router.register("customers", views.CustomerView, basename="customer")
router.register("orders", views.OrdersView, basename="orders")
router.register("rating", views.RatingView, basename="rating")


urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('product/<int:id>/', views.ProductDetailView.as_view()),
    path('product/search', views.ProductSearchFilter.as_view()),
    
    # path('register/', views.RegisterView.as_view()),
    # path('login/', views.LoginView.as_view()),
    # path('login/', TokenObtainPairView.as_view()),
    # path('login/refresh/', TokenRefreshView.as_view()),
] + router.urls
