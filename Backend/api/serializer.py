from rest_framework import serializers
from .models import Producto


class StockElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'precio', 'stock', 'categoria', 'imagen', 'descripcion']
