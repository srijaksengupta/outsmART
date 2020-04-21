from django.urls import path, include
from django.conf.urls import url

from . import views

app_name= 'products'

urlpatterns = [
    path('browse_products', views.browse_products, name='browse'),
    path('add_products', views.add_products, name='add'),
    path('my_listings',views.my_listings,name='listings'),
    path('my_orders',views.my_orders,name='orders'),
    path('manage_orders',views.manage_orders,name='manage_orders'),
    path('<int:product_id>',views.detail,name='detail'),
    url(r'^edit-product/(?P<pk>\d+)/$', views.edit_products, name='edit_products'),
    url(r'^delete-product/(?P<pk>\d+)/$', views.delete_products, name='delete_products'),
    path('wishlist', views.my_wishlist, name='wishlist'),
    path('add_wishlist', views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist', views.remove_wishlist, name='remove_wishlist'),
    path('cart', views.my_cart, name='cart'),
    path('order_summary', views.order_details, name="order_summary"),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    url(r'^item/edit-item/(?P<item_id>[-\w]+)/$', views.edit_item, name='edit_item'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^charge/$', views.charge, name='charge'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction_records, name='update_records'),
    url(r'^update-address/$', views.update_address, name='update_address'),
]
