from django.contrib import admin
from .models import Cart, Wishlist, Order

# Register your models here.

admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)