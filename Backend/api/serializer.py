from rest_framework import serializers
from .models import Product, Employee, Inventory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id_product', 'name', 'price', 'stock', 'category', 'image', 'description']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['ci', 'name', 'salary', 'id_boss']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id_inventory', 'category', 'id_warehouse']
