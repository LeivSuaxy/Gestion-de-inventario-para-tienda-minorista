from .models import Producto
from .serializer import ProductoSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from Backend.crudDB import CrudDB, ResponseType
from rest_framework import status


# Create your views here.
class TenItemsPaginator(PageNumberPagination):
    page_size: int = 5


@api_view(['GET'])
def get_objects(request):
    db = CrudDB()
    page = request.GET.get('page', 0)
    objects = db.get_response_elements(int(page))
    return objects


@api_view(['GET'])
def get_total_objects(request):
    db = CrudDB()
    objects = db.get_amount_elements_stock()
    return objects


@api_view(['POST'])
def insert_storage_in_database(request):
    name = request.data.get('name')
    location = request.data.get('location')
    if not name or not location:
        return Response({'error': 'Please provide both name and location'}, status=status.HTTP_400_BAD_REQUEST)
    db = CrudDB()
    response = db.create_storage(name, location)
    return response


@api_view(['POST'])
def insert_inventory_at_database(request):
    storage_name = request.data.get('storage')
    if not storage_name:
        return Response({'error': 'Please provide a database name'}, status=status.HTTP_400_BAD_REQUEST)
    db = CrudDB()
    response = db.create_inventory(storage_name)
    return response


@api_view(['POST'])
def insert_product_in_database(request):
    """
    Insert a product in the database
    JSON {
            product: {
                nombre: string,
                precio: float,
                stock: int,
                categoria: string,
                imagen: string,
                descripcion: string
            }
        }
    :param request:
    :return:
    """
    print(type(request.data))
    data: dict = request.data.get('product')
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    db = CrudDB()
    response = db.insert_product(data)
    return response
