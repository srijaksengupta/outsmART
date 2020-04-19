from django.forms import ModelForm
from .models import ProductPost, OrderItem, Order


class ProductPostForm(ModelForm):
    class Meta:
        model = ProductPost
        fields = ['title', 'summary', 'descrip', 'price', 'stock', 'image', 'tags']


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'city', 'state', 'country']
