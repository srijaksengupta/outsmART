from django.forms import ModelForm
from .models import ProductPost, OrderItem, Order
from django import forms

# Form for creating a product
class ProductPostForm(ModelForm):
    class Meta:
        model = ProductPost
        fields = ['title', 'summary', 'descrip', 'price', 'stock', 'image', 'tags']

# Form for setting the quantity of an item in an order
class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

# Form for the shipping information
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'city', 'state', 'country']

# Form for browsing products
class SearchForm(forms.Form):
    search = forms.CharField(required=False)
    CHOICES = (('Relevance', 'Relevance'),('Newest', 'Newest'),('Oldest', 'Oldest'))
    sortBy = forms.ChoiceField(choices=CHOICES)
    minPrice = forms.FloatField(required=False,initial=0)
    maxPrice = forms.FloatField(required=False,initial=999999)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()

        # Validation involving multiple fields
        if 'minPrice' in cleaned_data and 'maxPrice' in cleaned_data and cleaned_data['minPrice'] > cleaned_data['maxPrice']:
            self.add_error('maxPrice', 'maxPrice needs to be greater than minPrice')
        return cleaned_data

