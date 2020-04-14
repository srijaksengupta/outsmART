from django.urls import path, include

from . import views

app_name= 'products'

urlpatterns = [
    path('browse_products', views.browse_products, name='browse'),
    path('add_products', views.add_products, name='add'),
    path('my_listings',views.my_listings,name='listings'),
    path('<int:product_id>',views.detail,name='detail')
]
