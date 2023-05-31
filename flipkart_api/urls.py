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

    path('product/json', views.product_list),
    path('product/json/<int:pk>', views.product_detail),
    path('product/<int:pk>/category', views.CategoryList.as_view()),
    path('product/<int:pk>/category-create', views.CategoryCreate.as_view()),
    path('product/category/<int:pk>', views.CategoryDetail.as_view()),

    path('review/<str:username>', views.RatingView.as_view()), # 1st method
    path('review/', views.RatingView.as_view()), # 2nd method with ?username=tinu in url

] + router.urls
