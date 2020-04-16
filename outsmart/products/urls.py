from django.urls import path, include
from django.conf.urls import url

from . import views

app_name= 'products'

urlpatterns = [
    path('browse_products', views.browse_products, name='browse'),
    path('add_products', views.add_products, name='add'),
    path('my_listings',views.my_listings,name='listings'),
    url(r'^edit-product/(?P<pk>\d+)/$', views.edit_products, name='edit_products'),
    url(r'^delete-product/(?P<pk>\d+)/$', views.delete_products, name='delete_products'),
    path('<int:product_id>',views.detail,name='detail'),
    path('wishlist', views.my_wishlist, name='wishlist'),
    path('add_wishlist', views.add_wishlist, name='add_wishlist'),
    path('cart', views.my_cart, name='cart'),
]
