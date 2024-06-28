import psycopg2
from django.utils.timezone import now
from django.core.files.images import ImageFile
from api.models import Product
from api.serializer import ProductSerializer
from .settings import DATABASES, REST_FRAMEWORK
from enum import Enum
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
import math
from Backend.image_process import process_image
from django.http.request import QueryDict
import hashlib


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


# TODO REVIEW methods
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
    def register_user(self, ci: str, username: str, password: str) -> Response:
        """
        This method is used to register a new user in the database
        :param ci: The ci of the employee
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

            cursor.execute(f"SELECT 1 FROM employee WHERE ci='{ci}'")

            employee_exist = cursor.fetchone() is not None

            if not employee_exist:
                return Response({'not_found': 'The employee is not registered in the database'},
                                status.HTTP_404_NOT_FOUND)

            # Execute a SQL command to check if a user with the provided username already exists in the database
            cursor.execute(f"SELECT 1 FROM account WHERE user = '{username}'")

            # If the user exists, close the connection and return a code indicating that the user already exists
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # Generate Token
                token_string = ci + username + password

                token_hash = hashlib.sha256(token_string.encode()).hexdigest()

                password = hashlib.sha256(password.encode()).hexdigest()

                # If the user does not exist, insert a new record into the auth_user table with the provided username
                # and hashed password, along with some default values for other fields.
                try:
                    cursor.execute(f"""
                        INSERT INTO account VALUES ('{username}', '{password}', '{token_hash}', '{ci}')
                    """)
                except psycopg2.errors.UniqueViolation:
                    cursor.close()
                    connection.close()
                    return Response({'error': 'Please, this CI is already registered'},
                                    status.HTTP_409_CONFLICT)

                # Commit the changes
                connection.commit()
                # Close the cursor and the connection
                cursor.close()
                connection.close()

                # Return a success code
                return Response({'status': 'The user has been successfully registered',
                                 'token': token_hash}, status.HTTP_200_OK)
            else:
                # If the user exists, close the cursor and the connection and return a code indicating that the user
                # already exists
                cursor.close()
                connection.close()
                return Response({'status': 'You cannot register this user because it already exists.'},
                                status.HTTP_400_BAD_REQUEST)

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
            cursor.execute(f"SELECT 1 FROM account WHERE user = '{username}'")

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
                cursor.execute(f"SELECT password, auth_token FROM account WHERE user = '{username}'")
                result = cursor.fetchone()

                if result is not None:
                    user_password, auth_token = result
                else:
                    return ResponseType.NOT_FOUND.value

                # Process password
                password = hashlib.sha256(password.encode()).hexdigest()

                if password == user_password:
                    cursor.close()
                    connection.close()
                    return Response({'status': 'Login successfully', 'token': auth_token}, status.HTTP_200_OK)
                else:
                    # If the passwords do not match, close the cursor and the connection and return an error code
                    cursor.close()
                    connection.close()
                    return ResponseType.PASSWORD_INCORRECT.value

    def validate_token(self, username: str, auth_token: str) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        cursor.execute(f"SELECT auth_token FROM account WHERE username='{username}'")

        selected_token = cursor.fetchone()

        if not selected_token:
            return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)

        selected_token = selected_token[0]

        if selected_token == auth_token:
            return Response({'status': 'confirm'}, status.HTTP_200_OK)
        else:
            return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)

    # Function to get amount of elements from stock
    def get_amount_elements_stock(self) -> Response:

        # Connect to database
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection
        else:
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM product")

            self.total_elements_stock = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            return ResponseType.SUCCESS.value

    # Function to get elements from stock
    def get_elements_stock(self, pagination: int) -> Response:
        if pagination < 0:
            return ResponseType.ERROR.value

        pagination = pagination * REST_FRAMEWORK['PAGE_SIZE']

        # self.get_amount_elements_stock()

        if pagination < self.total_elements_stock:
            query = ("SELECT id_product, name, price, description, image, category, stock"
                     f" FROM product WHERE stock > 0 ORDER BY id_product "
                     f"LIMIT {REST_FRAMEWORK['PAGE_SIZE']} OFFSET {pagination}")
            elements = Product.objects.raw(query)

            if not elements:
                return ResponseType.NOT_FOUND.value
            else:
                serializer = ProductSerializer(elements, many=True)
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

        cursor.execute(f"INSERT INTO inventory (id_warehouse) VALUES ('{id_storage}')")
        connection.commit()

        cursor.close()
        connection.close()

        return ResponseType.SUCCESS.value

    def __get_storage_id__(self, storage_name) -> Response:
        connection = self.connect_to_db()

        if connection == ResponseType.ERROR.value:
            return connection

        cursor = connection.cursor()

        cursor.execute(f"SELECT id_warehouse FROM warehouse WHERE name='{storage_name}'")

        id_storage = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        if not id_storage:
            return ResponseType.NOT_FOUND.value
        else:
            return Response({'id_value': id_storage}, status.HTTP_200_OK)

    def update_purchased_products(self, products: QueryDict) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()

        for product in products:
            product_id = product['id']
            quantity = product['quantity']

            cursor.execute(f"UPDATE product SET stock=stock-{quantity} WHERE id_product={product_id}")

        connection.commit()
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

        cursor.execute(f"INSERT INTO client (ci, name, email, phone) SELECT '{client['ci']}', "
                       f"'{client['name']}',"
                       f"'{client['email']}', '{client['phone']}' WHERE NOT EXISTS (SELECT 1 FROM client WHERE "
                       f"ci='{client['ci']}')")

        # Orden de compra:
        cursor.execute(f"INSERT INTO purchase_order (date_done, total_amount, id_client)"
                       f"VALUES ('{now()}', {price_all_products_calct}, '{client['ci']}') RETURNING id_purchase_order")

        id_order = cursor.fetchone()[0]

        # Reporte
        cursor.execute(f"INSERT INTO report (report_date, id_employee) VALUES  ('{now()}', 1) RETURNING id_report")
        id_reporte = cursor.fetchone()[0]

        # Reporte de venta el cual tiene que hacer un reporte
        cursor.execute(f"INSERT INTO sales_report (id, date_time_delivery, total_amount, id_purchase_order)"
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

            cursor.execute(f"SELECT price FROM product WHERE id_product={product_id}")
            price = cursor.fetchone()[0]
            print(price)

            total_price += price * quantity

        cursor.close()
        connection.close()

        return Response({'total_price': total_price}, status=status.HTTP_200_OK)

    def search_products(self, search_query: str) -> Response:
        connection = self.connect_to_db()
        cursor = connection.cursor()
        query = f"SELECT * FROM product WHERE name LIKE %s"
        elements = Product.objects.raw(query, [f'%{search_query}%'])
        cursor.close()
        connection.close()

        if not elements:
            return ResponseType.NOT_FOUND.value
        else:
            serializer = ProductSerializer(elements, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
