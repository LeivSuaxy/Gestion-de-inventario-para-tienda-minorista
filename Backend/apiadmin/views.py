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
    response = crudAdmin.get_all_products()
    return response


# CREATE PRODUCTS
@api_view(['POST'])
def insert_product_in_database(request):
    data = request.data
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    if request.FILES.get('image') is not None:
        data['image'] = ImageFile(request.FILES['image'])
    response = crudAdmin.insert_product(data)
    return response


# UPDATE PRODUCTS
@api_view(['POST'])
def update_product_in_database(request):
    data = request.data
    print(type(data))
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    if 'image' in request.FILES:
        if request.FILES['image'] is not None:
            data['image'] = ImageFile(request.FILES['image'])
    response = crudAdmin.update_product(data)
    return response


# DELETE PRODUCTS
@api_view(['POST'])
def delete_product_in_database(request):
    data = request.data
    if not data:
        return Response({'error': 'Please provide a product'}, status=status.HTTP_400_BAD_REQUEST)
    response = crudAdmin.delete_product(data)
    return response


# <--Employees CRUD ENDPOINTS-->
# READ EMPLOYEES
@api_view(['GET'])
def get_all_employees(request):
    response = crudAdmin.get_all_employees()
    return response


# INSERT EMPLOYEE
@api_view(['POST'])
def insert_employee_to_database(request):
    data = request.data
    if not data or not data.get('employee'):
        return Response({'error': 'Please prove information about employee'}, status.HTTP_400_BAD_REQUEST)
    response = crudAdmin.insert_employee_in_database(data.get('employee'))
    return response


# UPDATE EMPLOYEE
def update_employee_in_database(request):
    pass


# DELETE EMPLOYEE
def delete_employee_in_database(request):
    pass


# TODO endpoint to get all reports
@api_view(['GET'])
def get_all_reports(request):
    pass


# TODO endpoint to get all inventories
@api_view(['GET'])
def get_all_inventories(request):
    pass


# TODO endpoint to get all warehouses
@api_view(['GET'])
def get_all_warehouses(request):
    pass
