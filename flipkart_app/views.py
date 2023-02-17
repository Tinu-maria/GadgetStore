from django.shortcuts import render, redirect
from django.views.generic import View, ListView, TemplateView, FormView
from django.contrib.auth.models import User
from flipkart_api.models import Product
from .models import Cart, Wishlist
from .forms import RegisterForm, LoginForm, CartForm, CheckoutForm, EnquiryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from .decorator import signin_required
from django.db.models import Q
from django.conf import settings
import stripe
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.


@method_decorator(signin_required, name="dispatch")
class ProductListView(ListView):
    """
    Returns list of products
    Gets product and wishlist context data
    """
    model = Product
    template_name = 'customer/product_list.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.all()

        paginator = Paginator(product, 6)
        page_num = self.request.GET.get('page', 1)
        products = paginator.page(page_num)

        wishlist = None
        if self.request.user:
            wishlist_object = Wishlist.objects.filter(user=self.request.user)
            wishlist = []
            for wish in wishlist_object:
                wishlist.append(wish.product)
        context = {
            "products": products,
            "wishlist": wishlist,
        }
        return context


@method_decorator(signin_required, name="dispatch")
class ProductDetailView(View):
    """
    In GET: Returns details of particular product
    In POST: Add a product to cart with required quantity
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Product.objects.get(id=id)

        cartlist = None
        if self.request.user:
            cartlist_object = Cart.objects.filter(user=self.request.user)
            cartlist = []
            for cart in cartlist_object:
                cartlist.append(cart.product)

        return render(request, 'customer/product_detail.html', {
            "form": CartForm(), "product": product, "cartlist": cartlist,
            })

    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = Product.objects.get(id=id)
        quantity = request.POST.get("quantity")
        user = request.user
        Cart.objects.create(product=product, user=user, quantity=quantity)
        return redirect("cart_list")


def search_product(request):
    """
    Search product with name
    """
    results = Product.objects.all()
    query = request.GET.get('search')
    if query:
        results = results.filter(Q(name__icontains=query))
    else:
        return redirect("list")
    context = {
        'results': results,
    }
    return render(request, 'customer/search.html', context)


class HomeView(TemplateView):
    """
    Returns home page of app
    """
    template_name = 'customer/home.html'


@method_decorator(signin_required, name="dispatch")
class CartListView(ListView):
    """
    Returns list of products in cart 
    """
    model = Cart
    template_name = "customer/cart_list.html"
    context_object_name = "carts"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).order_by("-created_date").exclude(status="Order-placed")


def cart_remove(request, id):
    """
    Remove a product from the cart
    """
    item_to_remove = Cart.objects.filter(id=id)
    if item_to_remove.exists():
        item_to_remove[0].delete()
        messages.success(request, "Product is removed from cart")
    return redirect("cart_list")


class DeliveryView(View):
    """
    In GET: Returns a registration page
    In POST: Creates a new user and redirect to login page
    """
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        return render(request, "customer/delivery.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            return redirect('checkout')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('delivery')
            

class CheckoutPaymentView(View):
    """
    Stripe payment to order products from cart
    """
    def get(self, request, *args, **kwargs):
    
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # id = kwargs.get('id')
        # prod = Product.objects.get(id=id)

        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items=[
                {
                    # 'price': prod.price,
                    'price': 'price_1MZYYRSIjmw4nsSsDnijagiE',
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            success_url = request.build_absolute_uri(reverse('checkout_success')) 
            + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = request.build_absolute_uri(reverse('checkout'))  
        )

        context = {
            "form": CheckoutForm(), 
            'session_id' : session.id,
            'stripe_public_key' : settings.STRIPE_PUBLISHABLE_KEY
            }
        
        return render(request, 'customer/checkout_payment.html', context)


def checkout_success(request):
    """
    Returns success page after payment
    """
    return render(request, 'customer/checkout_success.html')


def wish_add(request, *args, **kwargs):
    """
    Add a product to wishlist
    """
    id = kwargs.get("id")
    product = Product.objects.get(id=id)
    user = request.user
    Wishlist.objects.create(product=product, user=user)
    messages.success(request, "Product is added to wishlist")
    return redirect("wishlist")


def wish_remove(request, id):
    """
    Remove a product from the cart
    """
    item_to_remove = Wishlist.objects.filter(id=id)
    if item_to_remove.exists():
        item_to_remove[0].delete()
        messages.success(request, "Product is removed from wishlist")
    return redirect("wishlist")


@method_decorator(signin_required, name="dispatch")
class WishListView(ListView):
    """
    Returns list of favorite products
    """
    model = Wishlist
    template_name = "customer/wishlist.html"
    context_object_name = "wishs"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@method_decorator(signin_required, name="dispatch")
class EnquiryView(FormView):
    """
    Sends a enquiry message using html email
    Celery is added to schedule time
    """
    template_name = "customer/enquiry.html"
    form_class = EnquiryForm
    success_url = "enquiry/success"

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def enquiry_success(request):
    """
    Returns success page after enquiry
    """
    return render(request, 'customer/enquiry_success.html')


class RegisterView(View):
    """
    In GET: Returns a registration page
    In POST: Creates a new user and redirect to login page
    """
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "customer/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request, "New user created")
            return redirect('signin')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('register')


class LoginView(View):
    """
    In GET: Returns a login page
    In POST: Authenticate the user and then redirect to home page
    """
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "customer/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                context = {'username': username}
                messages.success(request, "Successfully logged in")
                return render(request, "customer/home.html", context)
            else:
                messages.error(request, "Invalid credentials")
                return redirect('signin')


@method_decorator(signin_required, name="dispatch")
class LogoutView(View):
    """
    User is logged out
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("signin")
