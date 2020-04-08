from django.db import models
from django.contrib.auth.models import User

def get_upload_path(instance, filename):
    return 'user-' + str(instance.owner.id) + '/' + filename

# Create your models here.
class ProductPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default="test")
    descrip = models.CharField(max_length=10000)
    stock = models.IntegerField(default=0)
    image = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    
    
