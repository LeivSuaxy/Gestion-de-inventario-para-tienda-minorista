from rest_framework import serializers
from api.models import (Product,
                        Warehouse,
                        Report,
                        SalesReport,
                        InventoryReport,
                        Messenger,
                        PurchaseOrder)


class ProductSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id_product', 'name', 'price', 'stock', 'category', 'image', 'description', 'id_inventory']


class WarehouseSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id_warehouse', 'name', 'location']


class ReportSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id_report', 'report_date', 'id_employee']


class SalesReportSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = SalesReport
        fields = ['id', 'date_time_delivery', 'total_amount', 'id_purchase_order', 'messenger']


class InventoryReportSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = InventoryReport
        fields = ['id', 'stock_amount', 'total_value', 'id_inventory']


class MessengerSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = Messenger
        fields = ['ci', 'vehicle', 'salary_per_km']


class PurchaseOrderSerializerAdmin(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id_purchase_order', 'date_done', 'total_amount', 'id_client', 'processed']
