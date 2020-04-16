from django.forms import ModelForm
from .models import ProductPost


class ProductPostForm(ModelForm):
    class Meta:
        model = ProductPost
        fields = ['title', 'summary', 'descrip', 'price', 'stock', 'image', 'tags']
