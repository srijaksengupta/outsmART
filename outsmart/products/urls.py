from django.urls import path, include

from . import views

app_name= 'products'

urlpatterns = [
    path('browse_products', views.browse_products, name='browse'),
    path('add_products', views.add_products, name='add'),
    path('my_listings',views.my_listings,name='listings'),
    path('<int:product_id>',views.detail,name='detail'),
    path('wishlist', views.my_wishlist, name='wishlist'),
    path('add_wishlist', views.add_wishlist, name='add_wishlist'),
    path('cart', views.my_cart, name='cart'),
]
