from django.db import models
from flipkart_api.models import Product
from django.contrib.auth.models import User

# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def total_price(self):
        return self.quantity * self.product.price


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cart = models.ManyToManyField(Cart)

    ordered_date = models.DateTimeField(auto_now_add=True)

    options= (
        ("Order-placed", "Order-placed"),
        ("Dispatched", "Dispatched"),
        ("In-transit", "In-transit"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled")
    )
    status = models.CharField(max_length=120, choices=options, default="Order-placed") 

    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.PositiveIntegerField(null=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.product.name
