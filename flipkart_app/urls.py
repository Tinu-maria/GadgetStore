from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product', views.ProductListView.as_view(), name='list'),
    path('product/<int:id>', views.ProductDetailView.as_view(), name='detail'),
    path('search', views.search_product, name='search'),

    path('cart_list', views.CartListView.as_view(), name='cart_list'), 
    path('cart_remove/<int:id>', views.cart_remove, name='cart_remove'),

    path('wish_add/<int:id>', views.wish_add, name='wish_add'), 
    path('wishlist', views.WishListView.as_view(), name='wishlist'), 
    path('wish_remove/<int:id>', views.wish_remove, name='wish_remove'),

    path('enquiry', views.EnquiryView.as_view(), name='enquiry'),
    path('enquiry/success', views.enquiry_success, name='enquiry_success'),

    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="signin"),
    path('logout', views.LogoutView.as_view(), name="signout"),

    path('delivery', views.DeliveryView.as_view(), name="delivery"),
    path('checkout', views.CheckoutPaymentView.as_view(), name='checkout'),
    path('checkout/success', views.checkout_success, name='checkout_success'),
]
