# Create your models here.
from django.db import models


class Client(models.Model):
    ci = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'client'


class Account(models.Model):
    user = models.CharField(primary_key=True, max_length=100, db_column='username')
    password = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=500)
    ci = models.OneToOneField('Employee', on_delete=models.CASCADE, db_column='ci')

    class Meta:
        db_table = 'account'


class PurchaseOrderDetail(models.Model):
    id_detail = models.AutoField(primary_key=True)
    purchase_order = models.ForeignKey('PurchaseOrder', models.DO_NOTHING, db_column='purchase_order')
    id_inventory = models.ForeignKey('Inventory', models.DO_NOTHING, db_column='id_inventory')
    quantity = models.IntegerField()  # Cantidad de objetos
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Precio total de compra

    class Meta:
        db_table = 'purchase_order_detail'


class Employee(models.Model):
    ci = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    id_boss = models.ForeignKey('self', on_delete=models.SET_NULL, db_column='id_boss', blank=True, null=True)

    class Meta:
        db_table = 'employee'


class Inventory(models.Model):
    id_inventory = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    id_warehouse = models.ForeignKey('Warehouse', on_delete=models.SET_NULL, db_column='id_warehouse', null=True,
                                     blank=True)

    class Meta:
        db_table = 'inventory'


class Warehouse(models.Model):
    id_warehouse = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)

    class Meta:
        db_table = 'warehouse'


class PurchaseOrder(models.Model):
    id_purchase_order = models.AutoField(primary_key=True)
    date_done = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client')

    class Meta:
        db_table = 'purchase_order'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(max_length=255, blank=True, null=True)
    id_inventory = models.ForeignKey(Inventory, models.SET_NULL, db_column='id_inventory', blank=True, null=True)
    category = models.CharField(max_length=255, db_column='category', blank=True, null=True)
    stock = models.IntegerField()

    class Meta:
        db_table = 'product'


class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    report_date = models.DateField()
    id_employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='id_employee')

    class Meta:
        db_table = 'report'


class InventoryReport(models.Model):
    id = models.OneToOneField(Report, models.DO_NOTHING, db_column='id', primary_key=True)
    id_inventory = models.ForeignKey(Inventory, models.DO_NOTHING, db_column='id_inventory')
    stock_amount = models.IntegerField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inventory_report'


class Messenger(models.Model):
    ci = models.OneToOneField(Employee, models.CASCADE, db_column='ci', primary_key=True)
    vehicle = models.CharField(max_length=255, null=True, blank=True)
    salary_per_km = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'messenger'


class SalesReport(models.Model):
    id = models.OneToOneField(Report, models.DO_NOTHING, db_column='id', primary_key=True)
    date_time_delivery = models.DateTimeField()
    id_purchase_order = models.ForeignKey(PurchaseOrder, models.DO_NOTHING, db_column='id_purchase_order')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    messenger = models.ForeignKey(Messenger, models.DO_NOTHING, db_column='messenger')

    class Meta:
        db_table = 'sales_report'
