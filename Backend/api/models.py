# Create your models here.
from django.db import models


# Create your models here.


class Cliente(models.Model):
    carnet_identidad = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'cliente'


class Cuenta(models.Model):
    usuario = models.CharField(primary_key=True, max_length=100)
    contrasegna = models.CharField(max_length=100)
    carnet_identidad = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='carnet_identidad')

    class Meta:
        db_table = 'cuenta'


class DetalleOrdenCompra(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_orden_compra = models.ForeignKey('OrdenCompra', models.DO_NOTHING, db_column='id_orden_compra')
    id_inventario = models.ForeignKey('Inventario', models.DO_NOTHING, db_column='id_inventario')
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_orden_compra'


class Empleado(models.Model):
    carnet_identidad = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=255)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    id_jefe = models.ForeignKey('self', models.DO_NOTHING, db_column='id_jefe', blank=True, null=True)

    class Meta:
        db_table = 'empleado'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    cantidad_stock = models.IntegerField()
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'inventario'


class OrdenCompra(models.Model):
    id_orden_compra = models.AutoField(primary_key=True)
    fecha_realizada = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        db_table = 'orden_compra'


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=100)
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario', blank=True, null=True)
    stock = models.IntegerField()

    class Meta:
        db_table = 'producto'


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    fecha_reporte = models.DateField()
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado')

    class Meta:
        db_table = 'reporte'


class ReporteInventario(models.Model):
    id = models.OneToOneField(Reporte, models.DO_NOTHING, db_column='id', primary_key=True)
    id_inventario = models.ForeignKey(Inventario, models.DO_NOTHING, db_column='id_inventario')
    cantidad_stock = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'reporte_inventario'


class ReporteVenta(models.Model):
    id = models.OneToOneField(Reporte, models.DO_NOTHING, db_column='id', primary_key=True)
    fecha_hora_entrega = models.DateTimeField()
    id_orden_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column='id_orden_compra')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'reporte_venta'
