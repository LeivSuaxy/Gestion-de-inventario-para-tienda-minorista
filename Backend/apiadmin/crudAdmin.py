import psycopg2.errors
from Backend.crudDB import CrudDB, ResponseType
from api.models import Producto, Empleado
from api.serializer import ProductoSerializer, EmpleadoSerializer
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
    query = "SELECT * FROM producto"
    elements = Producto.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = ProductoSerializer(elements, many=True)
    return Response({'elements': serializer.data}, status.HTTP_200_OK)


# CREATE PRODUCT

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

    # If the data has an inventory, I take the value of the category.
    if inventory is not None:
        cursor.execute(f"""
            SELECT categoria FROM inventario WHERE id_inventario={inventory}
        """)

        category = cursor.fetchone()[0]

    cursor.execute(f"""
        INSERT INTO producto (nombre, precio, stock, categoria, id_inventario, descripcion, imagen, fecha_entrada)
        VALUES ('{name}', {price}, {stock}, '{category}', {inventory}, '{description}', '{url_imagen}',
         '{now()}')
    """)

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
    entry_date = product_data.get('entry_date')

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
        UPDATE producto SET nombre='{name}', precio={price}, stock={int(stock)}, categoria='{category}', 
        id_inventario={inventory}, descripcion='{description}', imagen='{url_image}', fecha_entrada='{entry_date}'
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
    cursor.execute(f"DELETE FROM producto WHERE id_producto={id_product}")
    connection.commit()
    cursor.close()
    connection.close()
    return ResponseType.SUCCESS.value


# <--EMPLOYEES - CRUD-->
# READ
def get_all_employees() -> Response:
    query = "SELECT * FROM empleado"
    elements = Empleado.objects.raw(query)
    if not elements:
        return ResponseType.NOT_FOUND.value
    serializer = EmpleadoSerializer(elements, many=True)
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
                INSERT INTO empleado (carnet_identidad, nombre, salario, id_jefe)
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
                        INSERT INTO empleado (carnet_identidad, nombre, salario)
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
        UPDATE empleado SET nombre='{name}', salario={salary}, id_jefe='{boss}'
        WHERE carnet_identidad='{ci}'
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
        DELETE FROM empleado WHERE carnet_identidad='{ci}'
    """)
    connection.commit()
    cursor.close()
    connection.close()

    return ResponseType.SUCCESS.value


# TODO endpoint to get all reports
def get_all_reports() -> Response:
    pass


# TODO endpoint to get all inventories
def get_all_inventories() -> Response:
    pass


# TODO endpoint to get all warehouses
def get_all_warehouses() -> Response:
    pass
