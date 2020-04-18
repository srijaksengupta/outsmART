from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Create your models here.

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
    rating =  models.IntegerField(default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    sold = models.IntegerField(default=0)
    revenue = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    def __str__(self):
        return 'Product: {} by {}'.format(self.title,self.owner)


class OrderItem(models.Model):
    product = models.OneToOneField(ProductPost, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return 'Product: {} by {}'.format(self.product.title,self.product.owner)


class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price*item.quantity for item in self.items.all()])

    def get_tax(self):
        return round(0.1*sum([item.product.price*item.quantity for item in self.items.all()]))

    def get_shipping_charges(self):
        return 20.0

    def get_cart_total_plus_tax_plus_shipping(self):
        return sum([item.product.price*item.quantity for item in self.items.all()]) + \
               round(0.1*sum([item.product.price*item.quantity for item in self.items.all()])) + 20.0

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductPost, on_delete=models.CASCADE)
