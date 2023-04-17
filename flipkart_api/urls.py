from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register("productset", views.ProductsViewset)
router.register("category", views.CategoryViewset)
router.register("user", views.UserViewset)
router.register("profile", views.UserProfileViewset)
router.register("orders", views.OrdersViewset)
router.register("rating", views.RatingViewset)
router.register("savedproduct", views.SavedProductViewset)


urlpatterns = [
    path('product/', views.ProductView.as_view()),
    path('product/<int:id>/', views.ProductDetailView.as_view()),
    path('product/search', views.ProductSearchFilter.as_view()),
    path('saved-products/<int:pk>/', views.SavedProductView.as_view()),

    path('auth', obtain_auth_token), # here we get only token
    path('authenticate/', views.CustomObtainAuthToken.as_view()), # here we get user details along with token    

] + router.urls
