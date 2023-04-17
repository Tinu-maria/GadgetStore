from django.contrib import admin
from .models import Cart, Wishlist, Order

# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_filter = ('user', 'ordered')
    list_display = ('product', 'user', 'created_date', 'ordered')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_filter = ('user', )
    list_display = ('product', 'user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('user', 'ordered_date', 'status')
    list_display = ('product', 'user', 'status', 'ordered_date')
