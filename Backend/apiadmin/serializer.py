from rest_framework import serializers
from api.models import Product


class ProductSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id_product', 'name', 'price', 'stock', 'category', 'image', 'description', 'id_inventory']
