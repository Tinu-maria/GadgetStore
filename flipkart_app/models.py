from django.db import models
from flipkart_api.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    options = (
        ("In-cart", "In-cart"),
        ("Order-placed", "Order-placed"),
        ("Cancelled", "Cancelled")
    )
    status = models.CharField(max_length=120, choices=options, default="In-cart")
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.name


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
 
    def __str__(self):
        return self.address


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.ManyToManyField(Cart)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)   