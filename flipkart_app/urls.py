from django.urls import path
from . import views, tests

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product', views.ProductListView.as_view(), name='list'),
    path('product/<int:id>', views.ProductDetailView.as_view(), name='detail'),
    path('search', views.search_product, name='search'),

    path('mycart', views.CartListView.as_view(), name='cart_list'), 
    path('remove-from-cart/<int:id>', views.cart_remove, name='cart_remove'),

    path('add-to-wishlist/<int:id>', views.wish_add, name='wish_add'), 
    path('mywishlist', views.WishListView.as_view(), name='wishlist'), 
    path('remove-from-wishlist/<int:id>', views.wish_remove, name='wish_remove'),

    path('myorders', views.MyOrdersView.as_view(), name='myorders'), 
    path('orders/cancel/<int:id>', views.order_cancel, name='cancel_orders'), 
    path('profile/<int:id>', views.ProfileView.as_view(), name='profile'), 

    path('enquiry', views.EnquiryView.as_view(), name='enquiry'),
    path('enquiry/success', views.enquiry_success, name='enquiry_success'),

    path('register', views.RegisterView.as_view(), name="register"),
    path('login', views.LoginView.as_view(), name="signin"),
    path('logout', views.LogoutView.as_view(), name="signout"),

    path('placeorder/<int:cid>/<int:pid>', views.PlaceOrderView.as_view(), name="place_order"),
    path('checkout/', views.CheckoutPaymentView.as_view(), name='checkout'),
    # path('checkout/<int:cid>', views.CheckoutPaymentView.as_view(), name='checkout'),
    path('checkout/proceed', views.checkout_proceed, name='checkout_proceed'),
    path('checkout/success', views.checkout_success, name='checkout_success'),
    
    
    path("product-json", views.listing_product, name="product-json"),
    path("scroll-more", views.ProductListView.as_view(template_name="pagination/scroll-more.html"), name="scroll-more"),
    path("load-more", views.ProductListView.as_view(template_name="pagination/load-more.html"), name="load-more"),

]
