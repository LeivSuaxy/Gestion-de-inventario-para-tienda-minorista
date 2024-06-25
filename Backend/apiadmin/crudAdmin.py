import psycopg2.errors
from Backend.crudDB import CrudDB, ResponseType
from api.models import Product, Employee, Inventory
from api.serializer import EmployeeSerializer, InventorySerializer
from .serializer import ProductSerializerAdmin
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from django.core.files.images import ImageFile
from Backend.image_process import process_image
from django.utils.timezone import now


# TODO all endpoints of admin view
# TODO REVIEW alls URLS
# FIXME REVIEW alls POO items
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
def temp_insert_product(product_data: QueryDict) -> Response:
    # Obligatory columns
    if not product_data.get('name') or not product_data.get('price') or not product_data.get(
            'stock') or not product_data.get('description'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock, description',
                         'optional_fields': 'image, category, inventory'},
                        status=status.HTTP_400_BAD_REQUEST)

    columns = ', '.join(product_data.keys())
    placeholders = ', '.join(['%s'] * len(product_data))

    query = f"""INSERT INTO product ({columns}) VALUES ({placeholders})"""

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(query, tuple(product_data.values()))

    return ResponseType.SUCCESS.value


def insert_product(product_data: QueryDict) -> Response:
    # TODO check if product exists

    name = product_data.get('name')
    price = product_data.get('price')
    stock = product_data.get('stock')
    category = product_data.get('category')
    inventory = product_data.get('inventory')
    image: ImageFile = product_data.get('image')
    description = product_data.get('description')

    if not name or not price or not stock:
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock',
                         'optional_fields': 'description, image, category, inventory'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Processing data
    url_imagen = None
    if image is not None:
        url_imagen = process_image(image)

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    # TODO Here is the place to check if product exists and implements!

    # If the data has an inventory, I take the value of the category.
    if inventory is not None:
        try:
            cursor.execute(f"""
                SELECT category FROM inventory WHERE id_inventory={inventory}
            """)

            if category is None:
                category = cursor.fetchone()[0]
        except TypeError as e:
            print(e.args)
            cursor.close()
            connection.close()
            return Response({'not_found': 'The inventory you provided does not exist'}, status.HTTP_404_NOT_FOUND)

        try:
            cursor.execute(f"""
                INSERT INTO product (name, price, stock, category, id_inventory, description, image)
                VALUES ('{name}', {price}, {stock}, '{category}', {inventory}, '{description}', '{url_imagen}')
            """)
        except psycopg2.errors.UndefinedColumn as e:
            print(f'An error occurred executing the query in the database: {e.pgerror}')
            cursor.close()
            connection.close()
            return Response(
                {'conflict': 'There is a conflict with the database, check the console for more information'},
                status.HTTP_409_CONFLICT)
    else:
        if category is None:
            category = 'Others'

        try:
            cursor.execute(f"""
                       INSERT INTO product (name, price, stock, category, description, image)
                       VALUES ('{name}', {price}, {stock}, '{category}', '{description}', '{url_imagen}')
                   """)
        except psycopg2.errors.UndefinedColumn as e:
            print(f'An error occurred executing the query in the database: {e.pgerror}')
            cursor.close()
            connection.close()
            return Response(
                {'conflict': 'There is a conflict with the database, check the console for more information'},
                status.HTTP_409_CONFLICT)

    connection.commit()

    cursor.close()
    connection.close()

    return ResponseType.SUCCESS.value


# UPDATE PRODUCT
# FIXME the update product function
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

    if not name or not price or not stock or not category or not stock or not entry_date or not inventory:
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'name, price, stock, category, inventory, entry_date, inventory,',
                         'optional_fields': 'description, image'}, status=status.HTTP_400_BAD_REQUEST)

    # Processing data
    url_image = None
    if image is not None:
        print(type(image))
        url_image = process_image(image)

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""
        UPDATE product SET name='{name}', price={price}, stock={int(stock)}, category='{category}', 
        id_inventory={inventory}, description='{description}', image='{url_image}'
        WHERE id_producto={id_product}
    """)

    connection.commit()

    cursor.close()
    connection.close()

    return ResponseType.SUCCESS.value


# DELETE PRODUCT

def delete_product(data_id: QueryDict) -> Response:
    id_product = data_id.get('id')
    if not id_product:
        return Response({'error': 'Please provide an id of product you will delete'},
                        status=status.HTTP_400_BAD_REQUEST)
    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM product WHERE id_product={id_product}")
    connection.commit()
    cursor.close()
    connection.close()
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
# TODO REVIEW
def insert_employee_in_database(data: QueryDict) -> Response:
    ci = data.get('CI')
    name = data.get('name')
    salary = data.get('salary')
    boss = data.get('boss')

    if not ci or not name or not salary:
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'CI, name, salary',
                         'optional_fields': 'boss'}, status=status.HTTP_400_BAD_REQUEST)

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    if boss is not None:
        try:
            cursor.execute(f"""
                INSERT INTO employee (ci, name, salary, id_boss)
                VALUES ('{ci}', '{name}', {salary}, '{boss}')
            """)
        except psycopg2.errors.UniqueViolation as e:
            cursor.close()
            connection.close()
            print(e.pgerror)
            return Response({'error': 'El CI que esta introduciendo ya existe en la base de datos'},
                            status.HTTP_409_CONFLICT)
    else:
        try:
            cursor.execute(f"""
                        INSERT INTO employee (ci, name, salary)
                        VALUES ('{ci}', '{name}', {salary})
                    """)
        except psycopg2.errors.UniqueViolation as e:
            cursor.close()
            connection.close()
            print(e.pgerror)
            return Response({'error': 'El CI que esta introduciendo ya existe en la base de datos'},
                            status.HTTP_409_CONFLICT)

    connection.commit()
    cursor.close()
    connection.close()

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

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""
        UPDATE employee SET name='{name}', salary={salary}, id_boss='{boss}'
        WHERE ci='{ci}'
    """)

    connection.commit()
    cursor.close()
    connection.close()

    return ResponseType.SUCCESS.value


# DELETE
# FIXME fix the DELETE CASCADE
def delete_employee_in_database(ci: str) -> Response:
    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""
        DELETE FROM employee WHERE ci='{ci}'
    """)
    connection.commit()
    cursor.close()
    connection.close()

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
    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT 1 FROM warehouse WHERE id_warehouse='{storage_id}' 
    """)
    exist_storage = cursor.fetchone() is not None

    if not exist_storage:
        cursor.close()
        connection.close()
        return Response({'error': 'Please provide a valid warehouse'}, status.HTTP_404_NOT_FOUND)

    cursor.execute(f"""
        INSERT INTO inventory (category, id_warehouse) VALUES ('{category}', {storage_id})
    """)

    connection.commit()
    cursor.close()
    connection.close()

    return ResponseType.SUCCESS.value


# DELETE
def delete_inventory(id_inventory: int) -> Response:
    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    cursor.execute(f"""
        DELETE FROM inventory WHERE id_inventory={id_inventory}
    """)

    connection.commit()
    cursor.close()
    connection.close()
    return ResponseType.SUCCESS.value


# TODO endpoint to get all reports
def get_all_reports() -> Response:
    pass


# TODO endpoint to get all warehouses
def get_all_warehouses() -> Response:
    pass
