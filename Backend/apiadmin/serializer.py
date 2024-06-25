from rest_framework import serializers
from api.models import Producto


class ProductoSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'precio', 'stock', 'categoria', 'imagen', 'descripcion', 'id_inventario']
