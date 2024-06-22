from Backend.crudDB import CrudDB, ResponseType
from api.models import Producto, Empleado
from api.serializer import ProductoSerializer, EmpleadoSerializer
from rest_framework.response import Response
from rest_framework import status


# TODO all endpoints of admin view
def get_all_products() -> Response:
    query = "SELECT * FROM producto"
    elements = Producto.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = ProductoSerializer(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


def get_all_employees() -> Response:
    query = "SELECT * FROM empleado"
    elements = Empleado.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = EmpleadoSerializer(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# TODO endpoint to get all reports
def get_all_reports() -> Response:
    pass


# TODO endpoint to get all inventories
def get_all_inventories() -> Response:
    pass


# TODO endpoint to get all warehouses

def get_all_warehouses() -> Response:
    pass
