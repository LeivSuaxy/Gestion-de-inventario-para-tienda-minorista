from rest_framework import serializers
from .models import Producto, Empleado, Inventario


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'precio', 'stock', 'categoria', 'imagen', 'descripcion']


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['carnet_identidad', 'nombre', 'salario', 'id_jefe']


class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['id_inventario', 'categoria', 'id_almacen']
