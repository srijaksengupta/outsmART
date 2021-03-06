from django.db import models
from django.utils.timezone import now

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Model for a specific product
class ProductPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=200,default="No Summary")
    descrip = models.TextField(max_length=10000)
    stock = models.IntegerField(default=0)
    tags = models.CharField(max_length=10000)
    image = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(max_length=10, default=0.00)
    sold = models.IntegerField(default=0)
    revenue = models.FloatField(max_length=10,default= 0.00)

    def __str__(self):
        return 'Product: {} by {}'.format(self.title,self.owner)

# Model for an item in an order
class OrderItem(models.Model):
    product = models.ForeignKey(ProductPost, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return 'Product: {} by {} at {} qty {}'.format(self.product.title,self.product.owner, self.date_added, self.quantity)

# Model for an order containing multiple items
class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=10000)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    address_filled = models.BooleanField(default=False)
    total = models.DecimalField(default=0.00,decimal_places=2,max_digits=10)

    # Get all the different products in an order
    def get_cart_items(self):
        return self.items.all()

    # Get the price of all the items in the order
    def get_cart_total(self):
        if sum([item.product.price*item.quantity for item in self.items.all()]):
            return sum([item.product.price*item.quantity for item in self.items.all()])
        else:
            return None

    # Calculate tax for all items
    def get_tax(self):
        if sum([item.product.price*item.quantity for item in self.items.all()]):
            total = round(0.1*sum([item.product.price*item.quantity for item in self.items.all()]))
            return total
        else:
            return None

    # Calculate shipping for all items
    def get_shipping_charges(self):
        if sum([item.product.price * item.quantity for item in self.items.all()]):
            return 20.0
        else:
            return None

    # Add all fees together
    def get_cart_total_plus_tax_plus_shipping(self):
        if sum([item.product.price * item.quantity for item in self.items.all()]):

            return sum([item.product.price*item.quantity for item in self.items.all()]) + \
                   round(0.1*sum([item.product.price*item.quantity for item in self.items.all()])) + 20.0
        else:
            return None

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

# Model for all the transactions
class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.FloatField(max_length=100, default=0.0)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

# Model for a wishlist containing products
class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductPost, on_delete=models.CASCADE)
