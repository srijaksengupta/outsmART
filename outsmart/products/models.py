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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating =  models.IntegerField(default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    sold = models.IntegerField(default=0)
    revenue = models.DecimalField(default=0,max_digits=10, decimal_places=2)

    def __str__(self):
        return 'Product: {} by {}'.format(self.title,self.owner)
