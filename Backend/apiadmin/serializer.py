from rest_framework import serializers
from api.models import Product, Warehouse


class ProductSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id_product', 'name', 'price', 'stock', 'category', 'image', 'description', 'id_inventory']


class WarehouseSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id_warehouse', 'name', 'location']
