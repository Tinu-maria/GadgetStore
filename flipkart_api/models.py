from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="product_images", null=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/product/%i" % self.id


class Rating(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True)
    star = (
            (1, 'one'),
            (2, 'two'),
            (3, 'three'),
            (4, 'four'),
            (5, 'five'),
        )
    rating = models.PositiveSmallIntegerField(choices=star, null=True)


# from django_fsm import FSMField, transition
# import datetime 
# from django.db.models import Sum


# 1
# class UserValidityFsm(models.Model):
#     state = FSMField(default="active")
#     name = models.CharField(max_length=10)
#     date = models.DateField(auto_now_add=True)
#
#     @transition(field=state, source="active", target="occasional")
#     def state_to_progress(self):
#         if self.date < datetime.date.today():
#             return 'occasional'
#         else:
#             return 'active'
#
#     @transition(field=state, source="occasional", target="infrequent")
#     def state_to_progress(self):
#         if self.date < datetime.date.today():
#             return 'infrequent'
#         else:
#             return 'active'
#
#     @transition(field=state, source="infrequent", target="inactive")
#     def state_to_inactive(self):
#         pass


# 2
# class ProfileMixin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     class Meta:
#         abstract = True


# class ProfileModel(ProfileMixin, models.Model):
#     name = models.CharField(max_length=100)
#     created_date = models.DateTimeField(auto_now_add=True)

#     def pre_save(self):
#         self.name = self.name.upper()


# class ProductOrder(models.Model):
#     profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)

#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.profile = self.customer
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.profile.name

#     @staticmethod
#     def total_price():
#         total_price = ProductOrder.objects.aggregate(Sum('price'))['price__sum']
#         return total_price
