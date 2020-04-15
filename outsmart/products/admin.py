from django.contrib import admin

# Register your models here.
from .models import ProductPost
from .models import Wishlist


admin.site.register(ProductPost)
admin.site.register(Wishlist)