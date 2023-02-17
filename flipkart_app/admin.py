from django.contrib import admin
from .models import Cart, Wishlist, Checkout

# Register your models here.

admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Checkout)