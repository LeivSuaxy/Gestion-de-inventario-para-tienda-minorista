import psycopg2.errors
from Backend.crudDB import CrudDB, ResponseType
from api.models import Product, Employee, Inventory, Warehouse, SalesReport, Messenger
from api.serializer import EmployeeSerializer, InventorySerializer
import json

from .serializer import (ProductSerializerAdmin,
                         WarehouseSerializerAdmin,
                         SalesReportSerializerAdmin,
                         InventoryReportSerializerAdmin,
                         MessengerSerializerAdmin)
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from Backend.image_process import process_image
from psycopg2.extensions import connection as cnt, cursor as crs
from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile


# Private functions
def __close_connections__(connect: cnt, cursor_send: crs, commited: bool = False) -> None:
    cursor_send.close()
    if commited is not False:
        connect.commit()
    connect.close()


def __get_connections__() -> (cnt, crs):
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()
    return connection, cursor


# <--PRODUCTS - CRUD-->
# READ PRODUCTS

def get_all_products() -> Response:
    query = "SELECT * FROM product"
    elements = Product.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = ProductSerializerAdmin(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# CREATE PRODUCT
# CHECKED
def insert_product(product_data: QueryDict) -> Response:
    # Save
    product_data = product_data.copy()

    # Obligatory columns
    if not product_data.get('name') or not product_data.get('price') or not product_data.get(
            'stock') or not product_data.get('description'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock, description',
                         'optional_fields': 'image, category, id_inventory'},
                        status=status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    if product_data.get('category') is not None and product_data.get('id_inventory') is not None:
        pass
    elif product_data.get('category') is None:
        if product_data.get('id_inventory') is not None:
            try:
                cursor.execute(f"SELECT category FROM inventory WHERE id_inventory={product_data.get('id_inventory')}")
                category_inventory = cursor.fetchone()
                if category_inventory is not None:
                    category_inventory = category_inventory[0]
                    product_data['category'] = category_inventory
            except psycopg2.errors.ForeignKeyViolation as e:
                print(f'Error {e.pgerror}')
                __close_connections__(connect=connection, cursor_send=cursor)
                return Response({'error': 'The inventory you are entering does not exist',
                                 'code': e.pgcode},
                                status.HTTP_409_CONFLICT)
        else:
            product_data['category'] = 'Others'

    if product_data.get('image') is not None and type(product_data.get('image')) is InMemoryUploadedFile:
        image: ImageFile = product_data.get('image')
        url_imagen = process_image(image)
        product_data['image'] = url_imagen
    else:
        del product_data['image']

    columns = ', '.join(product_data.keys())
    placeholders = ', '.join(['%s'] * len(product_data))

    query = f"""INSERT INTO product ({columns}) VALUES ({placeholders})"""

    try:
        cursor.execute(query, tuple(product_data.values()))
        connection.commit()
    except psycopg2.errors.ForeignKeyViolation as e:
        print(f'Error {e.pgerror}')
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'The inventory you are entering does not exist',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)
    except psycopg2.errors.InvalidTextRepresentation as e:
        print(f'Error {e.pgerror}')
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'Please introduce correct values',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)

    __close_connections__(connect=connection, cursor_send=cursor)

    return ResponseType.SUCCESS.value


# UPDATE PRODUCT
# TODO ask frontend developer and TEST this method.
def update_product(product_data: QueryDict) -> Response:
    id_product = product_data.get('id_product')
    name = product_data.get('name')
    price = product_data.get('price')
    stock = product_data.get('stock')
    category = product_data.get('category')
    inventory = product_data.get('inventory')
    image = product_data.get('image')
    description = product_data.get('description')

    if not id_product:
        return Response({'error': 'Please provide the id of the product to update'},
                        status=status.HTTP_400_BAD_REQUEST)

    if not name or not price or not stock or not category or not stock or not inventory:
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock, category, inventory, entry_date, inventory,',
                         'optional_fields': 'description, image'}, status=status.HTTP_400_BAD_REQUEST)

    # Processing data
    url_image = None
    if image is not None:
        print(type(image))
        url_image = process_image(image)

    connection, cursor = __get_connections__()

    cursor.execute(f"""
        UPDATE product SET name='{name}', price={price}, stock={int(stock)}, category='{category}', 
        id_inventory={inventory}, description='{description}', image='{url_image}'
        WHERE id_producto={id_product}
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE PRODUCT
def delete_product(data: QueryDict) -> Response:
    if not data.get('elements'):
        return Response({'error': 'Please provide elements to delete'}, status.HTTP_400_BAD_REQUEST)
    datas: list = data.get('elements')

    connection, cursor = __get_connections__()
    for data in datas:
        if type(data) is int:
            cursor.execute(f"DELETE FROM product WHERE id_product={data}")

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)
    return ResponseType.SUCCESS.value


# <--EMPLOYEES - CRUD-->
# READ
# TODO Update serializer to messengers & employees or do view
def get_all_employees() -> Response:
    query = "SELECT * FROM employee"
    elements = Employee.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = EmployeeSerializer(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# INSERT
# CHECKED
def insert_employee_in_database(data: QueryDict) -> Response:
    if not data.get('ci') or not data.get('name') or not data.get('salary'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'ci, name, salary',
                         'optional_fields': 'id_boss'}, status=status.HTTP_400_BAD_REQUEST)

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))

    query = f"""INSERT INTO employee ({columns}) VALUES ({placeholders})"""

    connection, cursor = __get_connections__()

    try:
        cursor.execute(query, tuple(data.values()))
        connection.commit()
    except psycopg2.errors.UniqueViolation as e:
        __close_connections__(connect=connection, cursor_send=cursor)
        print(e.pgerror)
        return Response({'error': 'The CI you are entering already exists in the database',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)
    except psycopg2.errors.ForeignKeyViolation as e:
        __close_connections__(connect=connection, cursor_send=cursor)
        print(e.pgerror)
        return Response({'error': 'The employee to whom the id_boss corresponds does not exist',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)

    __close_connections__(connect=connection, cursor_send=cursor)

    return ResponseType.SUCCESS.value


# UPDATE
def update_employee_in_database(data: QueryDict) -> Response:
    ci = data.get('CI')
    name = data.get('name')
    salary = data.get('salary')
    boss = data.get('boss')

    if not ci or not name or not salary or not boss:
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'CI, name, salary, boss'}, status=status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    cursor.execute(f"""
        UPDATE employee SET name='{name}', salary={salary}, id_boss='{boss}'
        WHERE ci='{ci}'
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_employee_in_database(data: QueryDict) -> Response:
    if not data.get('employees'):
        return Response({'error': 'Please provide employees to delete'}, status.HTTP_400_BAD_REQUEST)

    employees: list = data.get('employees')

    connection, cursor = __get_connections__()

    for employee in employees:
        if type(employee) is str:
            cursor.execute(f"""
                DELETE FROM employee WHERE ci='{employee}'
            """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# <--INVENTORIES - CRUD-->
# READ
def get_all_inventories() -> Response:
    query = "SELECT * FROM inventory"
    elements = Inventory.objects.raw(query)
    if not elements:
        return Response({'error': 'is empty'}, status.HTTP_404_NOT_FOUND)
    serializer = InventorySerializer(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# INSERT
def insert_inventory(request_data: QueryDict) -> Response:
    category = request_data.get('category')
    storage_id = request_data.get('storage_id')

    if not category or not storage_id:
        return Response({'error': 'Please provide a category and a storage_id'}, status.HTTP_400_BAD_REQUEST)

    # Check if storage exists
    connection, cursor = __get_connections__()

    cursor.execute(f"""
        SELECT 1 FROM warehouse WHERE id_warehouse='{storage_id}' 
    """)
    exist_storage = cursor.fetchone() is not None

    if not exist_storage:
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'Please provide a valid warehouse'}, status.HTTP_404_NOT_FOUND)

    cursor.execute(f"""
        INSERT INTO inventory (category, id_warehouse) VALUES ('{category}', {storage_id})
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_inventory(data: QueryDict) -> Response:
    if not data.get('inventories'):
        return Response({'error': 'Please provide inventories to delete'}, status.HTTP_400_BAD_REQUEST)

    inventories: list = data.get('inventories')

    connection, cursor = __get_connections__()

    for inventory in inventories:
        if type(inventory) is int:
            cursor.execute(f"""
                    DELETE FROM inventory WHERE id_inventory={inventory}
            """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)
    return ResponseType.SUCCESS.value


# <--Reports - CRUD-->
# Sales Reports
def get_all_sales_reports() -> Response:
    query = "SELECT * FROM sales_report"
    elements = SalesReport.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = SalesReportSerializerAdmin(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# Inventories Reports
def get_all_inventory_reports() -> Response:
    query = "SELECT * FROM inventory_report"
    elements = SalesReport.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = InventoryReportSerializerAdmin(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# Generate inventories Reports
def generate_inventories_reports(data: QueryDict) -> Response:
    if not data.get('ci_employee'):
        return Response({'error': 'Please provide an ci_employee'}, status.HTTP_400_BAD_REQUEST)

    id_employee = data.get('ci_employee')
    # Cada reporte de inventario lleva: stock_amount: Cantidad de elementos en stock
    # total_value: La suma de la multiplication de la cantidad de elementos en stock por el precio
    # id_inventario al que corresponde.
    connection, cursor = __get_connections__()

    cursor.execute("""
        SELECT report_date FROM report 
        WHERE id_report=(SELECT id FROM inventory_report ORDER BY id DESC LIMIT 1)
    """)

    last_date = cursor.fetchone()

    if last_date is not None:
        last_date = last_date[0]

    if last_date == datetime.now().date():
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'You have already made the corresponding inventory reports on the day',
                         'status': 'not_today',
                         'last_date': last_date},
                        status.HTTP_400_BAD_REQUEST)

    cursor.execute("SELECT id_inventory FROM inventory")
    inventories = cursor.fetchall()

    if not inventories:
        __close_connections__(connect=connection, cursor_send=cursor)
    else:
        for inventory in inventories:
            id_inventory = inventory[0]

            cursor.execute(f"""
                INSERT INTO report (report_date, id_employee)
                VALUES ('{datetime.now()}', '{id_employee}')
                RETURNING id_report
            """)

            id_report = cursor.fetchone()[0]

            cursor.execute(f"""
                SELECT SUM(stock), SUM(price*stock)
                FROM product
                WHERE id_inventory={id_inventory}
            """)
            stock_sum, total_value = cursor.fetchone()

            cursor.execute(f"""
                INSERT INTO inventory_report (id, stock_amount, total_value, id_inventory)
                VALUES ({id_report}, {stock_sum}, {total_value}, {id_inventory})
            """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)
    return ResponseType.SUCCESS.value


def generate_sales_reports(data: QueryDict) -> Response:
    if not data.get('id_purchase_order') or not data.get('ci_employee'):
        return Response({'error': 'Please provide an id_purchase and a ci_employee'},
                        status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    # REVIEW require test
    cursor.execute(f"""
        SELECT total_amount, productos_comprados FROM purchase_order
        WHERE id_purchase_order={data.get('id_purchase_order')}
    """)

    data_self = data.copy()

    total_amount, purchase_products = cursor.fetchone()

    data_self['total_amount'] = total_amount
    data_self['productos_comprados'] = json.dumps(purchase_products)

    cursor.execute(f"""
        INSERT INTO report (report_date, id_employee)
        VALUES ('{datetime.now()}', '{data.get('ci_employee')}')
        RETURNING id_report
    """)

    data_self['id'] = cursor.fetchone()[0]

    del data_self['ci_employee']

    columns = ', '.join(data_self.keys())
    placeholders = ', '.join(['%s'] * len(data_self))

    query = f"""INSERT INTO sales_report ({columns}) VALUES ({placeholders})"""

    try:
        cursor.execute(query, tuple(data_self.values()))
        connection.commit()
    except psycopg2.errors.ForeignKeyViolation as e:
        print(f'Error {e.pgerror}')
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'The report id or purchase_order id is incorrect',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)

    __close_connections__(connect=connection, cursor_send=cursor)
    return ResponseType.SUCCESS.value


# <--Warehouses - CRUD-->
# READ
def get_all_warehouses() -> Response:
    query = "SELECT * FROM warehouse"
    elements = Warehouse.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = WarehouseSerializerAdmin(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# CREATE
def insert_warehouse(data: QueryDict) -> Response:
    if not data.get('name') or not data.get('location'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, location'}, status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM warehouse WHERE name='{data.get('name')}')")
    exist_storage = cursor.fetchone()

    if exist_storage:
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'There is already a warehouse with this name'}, status.HTTP_400_BAD_REQUEST)

    cursor.execute(f"""
        INSERT INTO warehouse (name, location) VALUES ('{data.get('name')}', '{data.get('location')}')
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# UPDATE
def update_warehouse(data: QueryDict) -> Response:
    if not data.get('id_warehouse') or not data.get('name') or not data.get('location'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'id_warehouse, name, location'}, status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    cursor.execute(f"""
        UPDATE warehouse SET name='{data.get("name")}', location='{data.get("location")}'
        WHERE id_warehouse={data.get('id_warehouse')}
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_warehouse(data: QueryDict) -> Response:
    if not data.get('warehouses'):
        return Response({'error': 'Please provide warehouses to delete'}, status.HTTP_400_BAD_REQUEST)

    warehouses: list = data.get('warehouses')

    connection, cursor = __get_connections__()

    for warehouse in warehouses:
        if type(warehouse) is int:
            cursor.execute(f'DELETE FROM warehouse WHERE id_warehouse={warehouse}')

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# <--Messenger - CRUD-->
# READ
def get_all_messengers() -> Response:
    query = 'SELECT * FROM messenger'
    elements = Messenger.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = MessengerSerializerAdmin(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# CREATE
def insert_messenger(data: QueryDict) -> Response:
    if not data.get('employee_ci') or not data.get('vehicle') or not data.get('salary_per_km'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'employee_id, vehicle, salary_per_km'}, status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    cursor.execute(f"""
        SELECT ci FROM employee WHERE ci='{data.get('employee_ci')}'
    """)

    employee_exists = cursor.fetchone()

    if not employee_exists:
        __close_connections__(connect=connection, cursor_send=cursor)
        return Response({'error': 'Please provide a CI that belongs to an employee'}, status.HTTP_400_BAD_REQUEST)

    cursor.execute(f"""
        INSERT INTO messenger (ci, vehicle, salary_per_km)
        VALUES ('{data.get('employee_ci')}', '{data.get('vehicle')}', {data.get('salary_per_km')}) 
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# UPDATE
def update_messenger(data: QueryDict) -> Response:
    if not data.get('employee_ci') or not data.get('vehicle') or not data.get('salary_per_km'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'employee_id, vehicle, salary_per_km'}, status.HTTP_400_BAD_REQUEST)

    connection, cursor = __get_connections__()

    cursor.execute(f"""
        UPDATE messenger SET vehicle='{data.get('vehicle')}', salary_per_km={data.get('salary_per_km')}
        WHERE ci='{data.get('employee_ci')}'
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_messenger(data: QueryDict) -> Response:
    if not data.get('messengers'):
        return Response({'error': 'Please provide messengers to delete'}, status.HTTP_400_BAD_REQUEST)

    messengers: list = data.get('messengers')

    connection, cursor = __get_connections__()

    for messenger in messengers:
        if type(messenger) is str:
            cursor.execute(f"DELETE FROM messenger WHERE ci='{messenger}'")

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# <--Complementary Methods-->
# Method to verify if it's possible to make an inventory report
def verify_reports_repeated() -> Response:
    connection, cursor = __get_connections__()

    cursor.execute("""
        SELECT report_date FROM report 
        WHERE id_report=(SELECT id FROM inventory_report ORDER BY id DESC LIMIT 1)
    """)

    last_date = cursor.fetchone()

    if last_date is not None:
        last_date = last_date[0]

        if last_date == datetime.now().date():
            __close_connections__(connect=connection, cursor_send=cursor)
            return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)

    return ResponseType.SUCCESS.value
