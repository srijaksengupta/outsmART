from django.contrib import admin

# Register your models here.
from .models import ProductPost, OrderItem, Order, Wishlist

admin.site.register(ProductPost)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Wishlist)
