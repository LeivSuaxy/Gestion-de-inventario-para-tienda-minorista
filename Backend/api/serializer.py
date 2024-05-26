from rest_framework import serializers
from .models import StockElement


class StockElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockElement
        fields = ['id', 'image', 'name', 'price', 'description', 'stock']
