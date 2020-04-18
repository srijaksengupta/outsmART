from django.contrib import admin

# Register your models here.
from .models import ProductPost, OrderItem, Order, Wishlist, Transaction

admin.site.register(ProductPost)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Wishlist)
