from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.images import ImageFile
from rest_framework import status

from apiadmin import crudAdmin


# Create your views here.

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
        return Response({'error': 'Please provide products'}, status=status.HTTP_400_BAD_REQUEST)
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
@api_view(['POST'])
def delete_employee_in_database(request):
    data = request.data
    if not data:
        return Response({'error': 'Please prove almost a ci to delete'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_employee_in_database(data)


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
    data = request.data
    if not data:
        return Response({'error': 'Please provide almost an id'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_inventory(data)


# <--REPORTS CRUD ENDPOINTS-->
# SALES REPORTS
@api_view(['GET'])
def get_all_sales_reports(request):
    return crudAdmin.get_all_sales_reports()


# INVENTORY REPORTS
@api_view(['GET'])
def get_all_inventory_reports(request):
    return crudAdmin.get_all_inventory_reports()


# Get Inventories Reports
@api_view(['POST'])
def generate_inventories_reports(request):
    return crudAdmin.generate_inventories_reports(request.data)


# Generate sales reports
@api_view(['POST'])
def generate_sales_reports(request):
    return crudAdmin.generate_sales_reports(request.data)


# Get all Purchase Orders
@api_view(['GET'])
def get_all_purchase_orders(request):
    return crudAdmin.get_all_purchase_orders()


# Delete purchase orders
@api_view(['POST'])
def delete_purchase_orders(request):
    return crudAdmin.delete_purchase_orders(request.data)


# <--WAREHOUSES CRUD ENDPOINTS-->
# READ
@api_view(['GET'])
def get_all_warehouses(request):
    return crudAdmin.get_all_warehouses()


# CREATE
@api_view(['POST'])
def insert_warehouse(request):
    return crudAdmin.insert_warehouse(request.data)


# UPDATE
@api_view(['POST'])
def update_warehouse(request):
    return crudAdmin.update_warehouse(request.data)


# DELETE
@api_view(['POST'])
def delete_warehouse(request):
    if not request.data:
        return Response({'error': 'Please provide almost an id_warehouse'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_warehouse(request.data)


# <--MESSENGER CRUD ENDPOINTS-->
# READ
@api_view(['GET'])
def get_all_messengers(request):
    return crudAdmin.get_all_messengers()


# CREATE
@api_view(['POST'])
def insert_messenger(request):
    return crudAdmin.insert_messenger(request.data)


# UPDATE
@api_view(['POST'])
def update_messenger(request):
    return crudAdmin.update_messenger(request.data)


# DELETE
@api_view(['POST'])
def delete_messenger(request):
    if not request.data:
        return Response({'error': 'Please provide almost a ci of the messenger'}, status.HTTP_400_BAD_REQUEST)
    return crudAdmin.delete_messenger(request.data)


# <--COMPLEMENTARY ENDPOINTS-->
@api_view(['GET'])
def verify_reports_repeated(request):
    return crudAdmin.verify_reports_repeated()
