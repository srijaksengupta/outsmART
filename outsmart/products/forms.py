from django.forms import ModelForm
from .models import ProductPost

class ProductPostForm(ModelForm):
    class Meta:
        model = ProductPost
        fields = ['descrip', 'image','title','stock','tags','price','summary']
        
        
