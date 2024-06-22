from Backend.Backend.crudDB import CrudDB, ResponseType
from Backend.api.models import Producto
from Backend.api.serializer import ProductoSerializer
from rest_framework.response import Response
from rest_framework import status


# TODO all endpoints of admin view
# TODO endpoint to get all products
def get_all_products() -> Response:
    connection = CrudDB().connect_to_db()
    cursor = connection.cursor()

    query = "SELECT * FROM producto"
    elements = Producto.objects.raw(query)

    if not elements:
        return ResponseType.NOT_FOUND.value

    serializer = ProductoSerializer(elements, many=True)

    return Response({'elements': serializer}, status.HTTP_200_OK)

# TODO endpoint to get all employees

# TODO endpoint to get all reports

# TODO endpoint to get all inventories

# TODO endpoint to get all warehouses
