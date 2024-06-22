import psycopg2
from django.utils.timezone import now
from django.core.files.images import ImageFile
from api.models import Producto
from api.serializer import ProductoSerializer
from .settings import DATABASES, REST_FRAMEWORK
from enum import Enum
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
import math
from Backend.image_process import process_image
from django.http.request import QueryDict


# Aquí se declararán las clases y funciones que se encargarán
# de realizar consultas a la base de datos

class ResponseType(Enum):
    # Caso que la operacion se realizó con éxito
    SUCCESS = Response({'status': 'Success'}, status=status.HTTP_200_OK)

    # Caso en que haya dado algun error
    ERROR = Response({'status': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    # Caso que no se encuentre ningun elemento
    NOT_FOUND = Response({'status': 'Not_found'}, status=status.HTTP_404_NOT_FOUND)

    # Caso que exista ya un elemento
    EXIST = Response({'status': 'founded'}, status=status.HTTP_409_CONFLICT)

    # Caso en que exista un error interno en la base de datos
    DATABASE_ERROR = Response({'status': 'Error conectando con la base de datos'}, status=status.HTTP_400_BAD_REQUEST)

    # Caso de contraseña mal escrita
    PASSWORD_INCORRECT = Response({'status': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)


class CrudDB:
    def __init__(self):
        self.total_elements_stock = 0
        self.get_amount_elements_stock()

    # Las funciones se realizarán dependiendo de la tabla que se quiera consultar
    @staticmethod
    def connect_to_db():
        try:
            conn = psycopg2.connect(
                host=DATABASES['default']['HOST'],
                database=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD']
            )
        except psycopg2.Error as e:
            print(f'Ocurrio un error: {e}')
            return ResponseType.DATABASE_ERROR.value

        return conn

    # Function to register users
    def register_user(self, username: str, password: str) -> Response:
        """
        This method is used to register a new user in the database
        :param username: The username of the new user
        :param password: The password of the new user.
        :return:A status code indicating the result of the opeation.
                It returns 200 if the operation is successful,
                400 if there is an error,
                or 409 if the user already exists.
        """

        # Connect to the database
        connection = self.connect_to_db()

        # If the connection is unsuccessful, return an error code
        if connection == ResponseType.DATABASE_ERROR.value:
            return connection
        else:
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()

            # Execute a SQL command to check if a user with the provided username already exists in the database
            cursor.execute(f"SELECT 1 FROM auth_user WHERE username = '{username}'")

            # If the user exists, close the connection and return a code indicating that the user already exists
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # If the user does not exist, insert a new record into the auth_user table with the provided username
                # and hashed password, along with some default values for other fields.
                cursor.execute(f"""
                    INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff,
                     is_active, date_joined) VALUES ('{password}', false, '{username}', '', '', '', false, true, now())
                """)

                # Commit the changes
                connection.commit()
                # Close the cursor and the connection
                cursor.close()
                connection.close()

                # Return a success code
                return ResponseType.SUCCESS.value
            else:
                # If the user exists, close the cursor and the connection and return a code indicating that the user
                # already exists
                cursor.close()
                connection.close()
                return ResponseType.EXIST.value

    # Function to log in users
    def log_in_user(self, username: str, password: str) -> Response:
        """
        This method is used to log in a user.


        :param username: The username of the user trying to log.
        :param password: The password provided by the user.
        :return: A status code indicating the result of the operation.
                It returns 200 if the operation is successful,
                400 if there is an error,
                or 404 if the user does not exist.
        """

        # Connect to the database
        connection = self.connect_to_db()

        # If the connection is unsuccessful, return an error code
        if connection == ResponseType.ERROR.value:
            return connection
        else:
            # Create a cursor object to execute SQL commands
            cursor = connection.cursor()

            # Execute a SQL command to check if a user with the provided username exists in the database
            cursor.execute(f"SELECT 1 FROM auth_user WHERE username = '{username}'")

            # If the user exists, close the connection and return a code indicating that the user already exists
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # If the user does not exist, close the cursor and the connection and return a code indicating that the
                # user does not exist
                cursor.close()
                connection.close()
                return ResponseType.NOT_FOUND.value
            else:
                # If the user exists, retrieve the hashed password of the user from the database
                cursor.execute(f"SELECT password FROM auth_user WHERE username = '{username}'")
                user_password = cursor.fetchone()[0]

                # Use Django's check_password function to compare the provided password with the stored hashed password
                if check_password(password, user_password):
                    # If the passwords match, close the cursor and the connection and return a success code
                    cursor.close()
                    connection.close()
                    return ResponseType.SUCCESS.value
                else:
                    # If the passwords do not match, close the cursor and the connection and return an error code
                    cursor.close()
                    connection.close()
                    return ResponseType.PASSWORD_INCORRECT.value

    # Function to get amount of elements from stock
    def get_amount_elements_stock(self) -> Response:

        # Connect to database
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection
        else:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM producto")

            self.total_elements_stock = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return ResponseType.SUCCESS.value

    # Function to get elements from stock
    def get_elements_stock(self, pagination: int) -> Response:
        if pagination < 0:
            return ResponseType.ERROR.value

        pagination = pagination * REST_FRAMEWORK['PAGE_SIZE']

        self.get_amount_elements_stock()
        # print('Total de elementos en stock: ', self.total_elements_stock)
        # print(f'Tamagno: {REST_FRAMEWORK["PAGE_SIZE"]}')

        if pagination < self.total_elements_stock:
            query = ("SELECT id_producto, nombre, precio, descripcion, imagen, categoria, stock"
                     f" FROM producto WHERE stock > 0 ORDER BY id_producto "
                     f"LIMIT {REST_FRAMEWORK['PAGE_SIZE']} OFFSET {pagination}")
            elements = Producto.objects.raw(query)

            if not elements:
                return ResponseType.NOT_FOUND.value
            else:
                serializer = ProductoSerializer(elements, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
        else:
            return ResponseType.ERROR.value

    def __get_urls__(self, pagination) -> Response:
        total_page = math.ceil(self.total_elements_stock / 5)

        if 0 <= pagination <= total_page:
            if (pagination + 1) >= total_page:
                next_page = None
            else:
                next_page = f'http://localhost:8000/api/public/objects/?page={pagination + 1}'

            if (pagination - 1) < 0:
                previous_page = None
            else:
                previous_page = f'http://localhost:8000/api/public/objects/?page={pagination - 1}'

            urls = {
                'next': next_page,
                'previous': previous_page
            }

            return Response(data=urls, status=status.HTTP_200_OK)
        else:
            return ResponseType.ERROR.value

    # Function to get elements and urls from stock with pagination. Is called by the get_objects view
    def get_response_elements(self, pagination: int) -> Response:
        if pagination < 0:
            return ResponseType.ERROR.value

        elements = self.get_elements_stock(pagination)

        if elements == ResponseType.ERROR.value:
            return elements

        urls = self.__get_urls__(pagination)

        if urls == ResponseType.ERROR.value:
            return urls

        data = {
            'elements': elements.data,
            'urls': urls.data
        }

        return Response(data=data, status=status.HTTP_200_OK)

    # Storage CRUD
    def create_storage(self, name, location) -> Response:
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        check = self.__exist_storage__(name)

        if check == ResponseType.ERROR.value:
            cursor.close()
            connection.close()
            return Response({'error': 'Ya existe el nombre'}, status.HTTP_400_BAD_REQUEST)

        cursor.execute(f"INSERT INTO almacen (nombre, ubicacion) VALUES ('{name}', '{location}')")
        connection.commit()

        cursor.close()
        connection.close()
        print('Insertado en la base de datos!')

        return ResponseType.SUCCESS.value

    def __exist_storage__(self, name) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM almacen WHERE nombre='{name}')")

        exist_storage = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not exist_storage:
            return ResponseType.SUCCESS.value
        else:
            return ResponseType.ERROR.value

    # Inventory CRUD
    def create_inventory(self, storage_name) -> Response:
        id_storage = self.__get_storage_id__(storage_name)

        if id_storage == ResponseType.ERROR.value or id_storage == ResponseType.NOT_FOUND.value:
            return id_storage

        id_storage = id_storage.data.get('id_value')

        print(id_storage)

        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        cursor.execute(f"INSERT INTO inventario (id_almacen) VALUES ('{id_storage}')")
        connection.commit()

        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def __get_storage_id__(self, storage_name) -> Response:
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        cursor.execute(f"SELECT id_almacen FROM almacen WHERE nombre='{storage_name}'")

        id_storage = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not id_storage:
            return ResponseType.NOT_FOUND.value
        else:
            return Response({'id_value': id_storage}, status.HTTP_200_OK)

    # TODO Endpoint to get inventories
    def get_inventories(self):
        pass

    # Product CRUD
    def insert_product(self, product_data: QueryDict) -> Response:
        # TODO check if product exists

        name = product_data.get('name')
        price = product_data.get('price')
        stock = product_data.get('stock')
        category = product_data.get('category')
        inventory = product_data.get('inventory')
        image: ImageFile = product_data.get('image')
        description = product_data.get('description')

        if not name or not price or not stock or not category or not inventory:
            return Response({'error': 'Please provide all the required fields',
                             'mandatory_fields': 'name, price, stock, category, inventory',
                             'optional_fields': 'description, image'}, status=status.HTTP_400_BAD_REQUEST)

        # Processing data
        url_imagen = None
        if image is not None:
            url_imagen = process_image(image)

        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute(f"""
            INSERT INTO producto (nombre, precio, stock, categoria, id_inventario, descripcion, imagen, fecha_entrada)
            VALUES ('{name}', {price}, {stock}, '{category}', {inventory}, '{description}', '{url_imagen}',
             '{now()}')
        """)

        connection.commit()

        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def get_product(self):
        pass

    # FIXME the update product function
    def update_product(self, product_data: QueryDict) -> Response:
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

        connection = self.connect_to_db()
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

    def update_purchased_products(self, products: QueryDict) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        for product in products:
            product_id = product['id']
            quantity = product['quantity']

            cursor.execute(f"UPDATE producto SET stock=stock-{quantity} WHERE id_producto={product_id}")

        connection.commit()
        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def delete_product(self, data_id: QueryDict) -> Response:
        id_product = data_id.get('id')
        if not id_product:
            return Response({'error': 'Please provide an id of product you will delete'},
                            status=status.HTTP_400_BAD_REQUEST)
        connection = self.connect_to_db()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM producto WHERE id_producto={id_product}")
        connection.commit()
        self.total_elements_stock -= 1
        cursor.close()
        connection.close()
        return ResponseType.SUCCESS.value

    def process_purchases(self, data: QueryDict) -> Response:
        client = data.get('client')
        products = data.get('products')

        if not client:
            return Response({'error': 'Please provide the client information',
                             'required_fields:': 'ci, name, email, phone'}, status=status.HTTP_400_BAD_REQUEST)

        if not products:
            return Response({'error': 'Please provide the products to purchase',
                             'required_fields': '[id, quantity]'}, status=status.HTTP_400_BAD_REQUEST)

        # Reporte de venta: id, fecha, total, id_orden_compra
        # Orden de compra: id, fecha, total, id_cliente
        # Cliente: CI, nombre, email, telefono

        # Price_all_products
        price_all_products_calct = self.__process_total_price_products_purchased__(products).data['total_price']

        connection = self.connect_to_db()
        cursor = connection.cursor()

        # Agnadir cliente if not exists

        cursor.execute(f"INSERT INTO cliente (carnet_identidad, nombre, email, telefono) SELECT '{client['ci']}', "
                       f"'{client['name']}',"
                       f"'{client['email']}', '{client['phone']}' WHERE NOT EXISTS (SELECT 1 FROM Cliente WHERE "
                       f"carnet_identidad='{client['ci']}')")

        # Orden de compra:
        cursor.execute(f"INSERT INTO orden_compra (fecha_realizada, monto_total, id_cliente)"
                       f"VALUES ('{now()}', {price_all_products_calct}, '{client['ci']}') RETURNING id_orden_compra")

        id_order = cursor.fetchone()[0]

        # Reporte
        cursor.execute(f"INSERT INTO reporte (fecha_reporte, id_empleado) VALUES  ('{now()}', 1) RETURNING id_reporte")
        id_reporte = cursor.fetchone()[0]

        # Reporte de venta el cual tiene que hacer un reporte
        cursor.execute(f"INSERT INTO reporte_venta (id, fecha_hora_entrega, monto_total, id_orden_compra)"
                       f" VALUES ({id_reporte}, '{now()}', {price_all_products_calct}, {id_order})")

        connection.commit()

        cursor.close()
        connection.close()
        return Response({'total_price': price_all_products_calct}, status=status.HTTP_200_OK)

    def __process_total_price_products_purchased__(self, products: list) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        print(products)

        total_price = 0

        for product in products:
            product_id = product['id']
            quantity = product['quantity']

            cursor.execute(f"SELECT precio FROM producto WHERE id_producto={product_id}")
            price = cursor.fetchone()[0]
            print(price)

            total_price += price * quantity

        cursor.close()
        connection.close()

        return Response({'total_price': total_price}, status=status.HTTP_200_OK)

    def search_products(self, search_query: str) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()
        query = f"SELECT * FROM producto WHERE nombre LIKE %s"
        elements = Producto.objects.raw(query, [f'%{search_query}%'])
        cursor.close()
        connection.close()

        if not elements:
            return ResponseType.NOT_FOUND.value
        else:
            serializer = ProductoSerializer(elements, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
