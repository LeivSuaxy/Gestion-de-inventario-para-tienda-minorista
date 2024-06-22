from django.shortcuts import render
from rest_framework.decorators import api_view

from apiadmin import crudAdmin


# from Backend.apiadmin import crudAdmin as db


# Create your views here.

# TODO all endpoints of admin view
@api_view(['GET'])
def get_all_products(request):
    response = crudAdmin.get_all_products()
    return response


@api_view(['GET'])
def get_all_employees(request):
    response = crudAdmin.get_all_employees()
    return response


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
