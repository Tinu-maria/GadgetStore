from django.contrib import admin
from .models import Product, Rating, Category, UserProfile,  SavedProduct

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'phone')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ('rating', )
    list_display = ('title', 'description', 'rating')


@admin.register(SavedProduct)
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('currentuser', 'product')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('category_name', )
    list_display = ('product', 'category_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    def category_name(self, object):
        category = object.category.first()
        return category.category_name if category else 'Null'
    
    list_filter = ('price', 'seller')
    list_display = ('name', 'price', 'category_name', 'seller')


# Task

# @admin.register(Addon)
# class AddonAdmin(admin.ModelAdmin):
#     list_filter = ('date', )
#     list_display = ('bio', 'date')


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
    
#     def addon_date(self, object):
#         return object.addon.addon_date
    
#     list_filter = ('price', )
#     list_display = ('name', 'price', 'addon_date')