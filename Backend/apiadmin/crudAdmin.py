import psycopg2.errors
from Backend.crudDB import CrudDB, ResponseType
from api.models import Product, Employee, Inventory, Warehouse, SalesReport, Messenger
from api.serializer import EmployeeSerializer, InventorySerializer
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


def __close_connections__(connect: cnt, cursor_send: crs, commited: bool = False):
    cursor_send.close()
    if commited is not False:
        connect.commit()
    connect.close()


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
    # Obligatory columns
    if not product_data.get('name') or not product_data.get('price') or not product_data.get(
            'stock') or not product_data.get('description'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock, description',
                         'optional_fields': 'image, category, id_inventory'},
                        status=status.HTTP_400_BAD_REQUEST)

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()
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

    if product_data.get('image') is not None:
        image: ImageFile = product_data.get('image')
        url_imagen = process_image(image)
        product_data['image'] = url_imagen

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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        UPDATE product SET name='{name}', price={price}, stock={int(stock)}, category='{category}', 
        id_inventory={inventory}, description='{description}', image='{url_image}'
        WHERE id_producto={id_product}
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE PRODUCT

def delete_product(data_id: QueryDict) -> Response:
    id_product = data_id.get('id')
    if not id_product:
        return Response({'error': 'Please provide an id of product you will delete'},
                        status=status.HTTP_400_BAD_REQUEST)
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()
    cursor.execute(f"DELETE FROM product WHERE id_product={id_product}")
    __close_connections__(connect=connection, cursor_send=cursor, commited=True)
    return ResponseType.SUCCESS.value


# DELETE PRODUCTS
def delete_more_than_one_product(data: QueryDict) -> Response:
    if not data.get('elements'):
        return Response({'error': 'Please provide elements to delete'}, status.HTTP_400_BAD_REQUEST)
    datas: list = data.get('elements')

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()
    for data in datas:
        if type(data) is int:
            cursor.execute(f"DELETE FROM product WHERE id_product={data}")

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)
    return ResponseType.SUCCESS.value


# <--EMPLOYEES - CRUD-->
# READ
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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        UPDATE employee SET name='{name}', salary={salary}, id_boss='{boss}'
        WHERE ci='{ci}'
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_employee_in_database(ci: str) -> Response:
    connection: cnt = CrudDB.connect_to_db()
    cursor:crs = connection.cursor()

    cursor.execute(f"""
        DELETE FROM employee WHERE ci='{ci}'
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
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

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
def delete_inventory(id_inventory: int) -> Response:
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        DELETE FROM inventory WHERE id_inventory={id_inventory}
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
    # Primero, se realiza la llamada al methods
    if not data.get('ci_employee'):
        return Response({'error': 'Please provide an ci_employee'}, status.HTTP_400_BAD_REQUEST)

    id_employee = data.get('ci_employee')
    # Cada reporte de inventario lleva: stock_amount: Cantidad de elementos en stock
    # total_value: La suma de la multiplication de la cantidad de elementos en stock por el precio
    # id_inventario al que corresponde.
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        UPDATE warehouse SET name='{data.get("name")}', location='{data.get("location")}'
        WHERE id_warehouse={data.get('id_warehouse')}
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_warehouse(id_warehouse: int) -> Response:
    if not id_warehouse:
        return Response({'error': 'Please provide an id to delete warehouse'}, status.HTTP_400_BAD_REQUEST)

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f'DELETE FROM warehouse WHERE id_warehouse={id_warehouse}')

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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        SELECT ci FROM employee WHERE ci='{data.get('employee_ci')}'
    """)

    employee_exists = cursor.fetchone()

    if not employee_exists:
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

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"""
        UPDATE messenger SET vehicle='{data.get('vehicle')}', salary_per_km={data.get('salary_per_km')}
        WHERE ci='{data.get('employee_ci')}'
    """)

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# DELETE
def delete_messenger(ci: str) -> Response:
    if not ci:
        return Response({'error': 'Please prove a ci to delete messenger'}, status.HTTP_400_BAD_REQUEST)

    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

    cursor.execute(f"DELETE FROM messenger WHERE ci='{ci}'")

    __close_connections__(connect=connection, cursor_send=cursor, commited=True)

    return ResponseType.SUCCESS.value


# <--Complementary Methods-->
# Method to verify if it's possible to make an inventory report
def verify_reports_repeated() -> Response:
    connection: cnt = CrudDB.connect_to_db()
    cursor: crs = connection.cursor()

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
