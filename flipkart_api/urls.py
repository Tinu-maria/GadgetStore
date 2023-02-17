from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register("productset", views.ProductsViewset, basename="productset")

urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('product/<int:id>/', views.ProductDetailView.as_view()),
    path('product/search', views.ProductSearchFilter.as_view()),
    
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    # path('login/', TokenObtainPairView.as_view()),
    # path('login/refresh/', TokenRefreshView.as_view()),
] + router.urls
