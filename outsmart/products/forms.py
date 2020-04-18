from django.forms import ModelForm
from .models import ProductPost, OrderItem


class ProductPostForm(ModelForm):
    class Meta:
        model = ProductPost
        fields = ['title', 'summary', 'descrip', 'price', 'stock', 'image', 'tags']


class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
