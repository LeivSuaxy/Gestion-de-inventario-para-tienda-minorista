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
    print(elements)
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

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    if product_data.get('category') is None:
        if product_data.get('id_inventory') is not None:
            try:
                cursor.execute(f"SELECT category FROM inventory WHERE id_inventory={product_data.get('id_inventory')}")
                category_inventory = cursor.fetchone()
                if category_inventory is not None:
                    category_inventory = category_inventory[0]
                    product_data['category'] = category_inventory
            except psycopg2.errors.ForeignKeyViolation as e:
                print(f'Error {e.pgerror}')
                cursor.close()
                connection.close()
                return Response({'error': 'The inventory you are entering does not exist',
                                 'code': e.pgcode},
                                status.HTTP_409_CONFLICT)
        else:
            product_data["category"] = "Others"

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
        cursor.close()
        connection.close()
        return Response({'error': 'The inventory you are entering does not exist',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)

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
# CHECKED
def insert_employee_in_database(data: QueryDict) -> Response:
    if not data.get('ci') or not data.get('name') or not data.get('salary'):
        return Response({'error': 'Please provide all the required fields',
                         'mandatory_fields': 'ci, name, salary',
                         'optional_fields': 'id_boss'}, status=status.HTTP_400_BAD_REQUEST)

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))

    query = f"""INSERT INTO employee ({columns}) VALUES ({placeholders})"""

    connection = CrudDB.connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute(query, tuple(data.values()))
        connection.commit()
    except psycopg2.errors.UniqueViolation as e:
        cursor.close()
        connection.close()
        print(e.pgerror)
        return Response({'error': 'The CI you are entering already exists in the database',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)
    except psycopg2.errors.ForeignKeyViolation as e:
        cursor.close()
        connection.close()
        print(e.pgerror)
        return Response({'error': 'The employee to whom the id_boss corresponds does not exist',
                         'code': e.pgcode},
                        status.HTTP_409_CONFLICT)

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
