from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class StockElement(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.ImageField(upload_to='stock')
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    stock = models.IntegerField()


