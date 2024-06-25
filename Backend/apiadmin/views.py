from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.images import ImageFile
from rest_framework import status

from apiadmin import crudAdmin


# from Backend.apiadmin import crudAdmin as db


# Create your views here.

# TODO all endpoints of admin view

# <--PRODUCTS CRUD ENDPOINTS-->
# READ PRODUCTS
@api_view(['GET'])
def get_all_products(request):
    return crudAdmin.get_all_products()


# CREATE PRODUCTS
@api_view(['POST'])
def insert_product_in_database(request):
    return crudAdmin.insert_product(request.data)


# UPDATE PRODUCTS
@api_view(['POST'])
def update_product_in_database(request):
    data = request.data
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    if 'image' in request.FILES:
        if request.FILES['image'] is not None:
            data['image'] = ImageFile(request.FILES['image'])
    return crudAdmin.update_product(data)


# DELETE PRODUCTS
@api_view(['POST'])
def delete_product_in_database(request):
    data = request.data
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_product(data)


# <--Employees CRUD ENDPOINTS-->
# READ EMPLOYEES
@api_view(['GET'])
def get_all_employees(request):
    return crudAdmin.get_all_employees()


# INSERT EMPLOYEE
@api_view(['POST'])
def insert_employee_to_database(request):
    data = request.data
    if not data or not data.get('employee'):
        return Response({'error': 'Please prove information about employee'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.insert_employee_in_database(data.get('employee'))


# UPDATE EMPLOYEE
@api_view(['POST'])
def update_employee_in_database(request):
    data = request.data
    if not data.get('employee'):
        return Response({'error': 'Please prove information about employee'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.update_employee_in_database(data.get('employee'))


# DELETE EMPLOYEE
# FIXME Review delete cascade
@api_view(['POST'])
def delete_employee_in_database(request):
    data = request.data
    if not data.get('ci'):
        return Response({'error': 'Please prove a ci to delete'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_employee_in_database(data.get('ci'))


# <--INVENTORIES CRUD ENDPOINTS-->
# READ INVENTORIES
@api_view(['GET'])
def get_all_inventories(request):
    return crudAdmin.get_all_inventories()


# INSERT INVENTORY
@api_view(['POST'])
def insert_inventory_in_database(request):
    data = request.data
    return crudAdmin.insert_inventory(data)


# DELETE INVENTORY
@api_view(['POST'])
def delete_inventory_from_database(request):
    id_inventory = request.data.get('id')
    if not id_inventory:
        return Response({'error': 'Please provide an id'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_inventory(id_inventory)


# TODO endpoint to get all reports
@api_view(['GET'])
def get_all_reports(request):
    pass


# TODO endpoint to get all warehouses
@api_view(['GET'])
def get_all_warehouses(request):
    pass


@api_view(['POST'])
def insert_warehouse(request):
    pass
