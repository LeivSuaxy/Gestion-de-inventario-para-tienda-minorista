import json

import psycopg2
from django.utils.timezone import now
from api.models import Product
from api.serializer import ProductSerializer
from .settings import DATABASES, REST_FRAMEWORK
from enum import Enum
from rest_framework.response import Response
from rest_framework import status
import math
from django.http.request import QueryDict
import hashlib
from datetime import datetime, timedelta
from psycopg2.extensions import cursor as crs, connection as cnt


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

    @staticmethod
    def __close_connections__(connect: cnt, cursor_send: crs, commited: bool = False):
        cursor_send.close()
        if commited is not False:
            connect.commit()
        connect.close()

    @staticmethod
    def update_purchased_products(products: QueryDict, cursor: crs) -> Response:

        for product in products:
            product_id = product['id']
            quantity = product['quantity']

            cursor.execute(f"UPDATE product SET stock=stock-{quantity} WHERE id_product={product_id}")

        return ResponseType.SUCCESS.value

    # Function to register users
    def register_user(self, ci: str, username: str, password: str) -> Response:
        # Connect to the database
        connection: cnt = self.connect_to_db()

        # Create a cursor object to execute SQL commands
        cursor: crs = connection.cursor()

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

            expiration_time = datetime.now() + timedelta(minutes=20)

            # If the user does not exist, insert a new record into the auth_user table with the provided username
            # and hashed password, along with some default values for other fields.
            try:
                cursor.execute(f"""
                    INSERT INTO account
                    VALUES ('{username}', '{password}', '{token_hash}', '{ci}', '{expiration_time}') 
                """)
            except psycopg2.errors.UniqueViolation:
                self.__close_connections__(connect=connection, cursor_send=cursor)
                return Response({'error': 'Please, this CI is already registered'},
                                status.HTTP_409_CONFLICT)

            # Commit the changes
            self.__close_connections__(connect=connection, cursor_send=cursor, commited=True)

            # Return a success code
            return Response({'status': 'The user has been successfully registered',
                             'token': token_hash}, status.HTTP_200_OK)
        else:
            # If the user exists, close the cursor and the connection and return a code indicating that the user
            # already exists
            self.__close_connections__(connect=connection, cursor_send=cursor)
            return Response({'status': 'You cannot register this user because it already exists.'},
                            status.HTTP_400_BAD_REQUEST)

    # Function to log in users
    def log_in_user(self, username: str, password: str) -> Response:
        # Connect to the database
        connection: cnt = self.connect_to_db()

        # Create a cursor object to execute SQL commands
        cursor: crs = connection.cursor()
        # Execute a SQL command to check if a user with the provided username exists in the database
        cursor.execute(f"""
            SELECT username FROM account WHERE username='{username}'
        """)
        # If the user exists, close the connection and return a code indicating that the user already exists
        user_exists = cursor.fetchone() is not None

        if not user_exists:
            # If the user does not exist, close the cursor and the connection and return a code indicating that the
            # user does not exist
            self.__close_connections__(connect=connection, cursor_send=cursor)
            return ResponseType.NOT_FOUND.value
        else:
            # If the user exists, retrieve the hashed password of the user from the database
            cursor.execute(f"SELECT password, auth_token FROM account WHERE username = '{username}'")
            result = cursor.fetchone()

            if result is not None:
                user_password, auth_token = result
            else:
                return ResponseType.NOT_FOUND.value

            # Process password
            password = hashlib.sha256(password.encode()).hexdigest()

            if password == user_password:
                expiration_time = datetime.now() + timedelta(minutes=20)

                cursor.execute(f"""
                    UPDATE account SET token_expiration='{expiration_time}' WHERE username='{username}'
                """)
                self.__close_connections__(connect=connection, cursor_send=cursor, commited=True)
                return Response({'status': 'Login successfully', 'token': auth_token}, status.HTTP_200_OK)
            else:
                # If the passwords do not match, close the cursor and the connection and return an error code
                self.__close_connections__(connect=connection, cursor_send=cursor)
                return ResponseType.PASSWORD_INCORRECT.value

    # Function to validate token
    def validate_token(self, username: str, auth_token: str) -> Response:
        connection: cnt = self.connect_to_db()
        cursor: crs = connection.cursor()

        cursor.execute(f"SELECT auth_token, token_expiration FROM account WHERE username='{username}'")

        selected_token, token_expiration = cursor.fetchone()

        if not selected_token:
            self.__close_connections__(connect=connection, cursor_send=cursor)
            return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)

        selected_token = selected_token[0]

        if selected_token == auth_token:
            if datetime.now() < token_expiration:
                expiration_time = datetime.now() + timedelta(minutes=20)
                cursor.execute(f"""
                    UPDATE account SET (token_expiration='{expiration_time}' WHERE username='{username}')
                    """)
                self.__close_connections__(connect=connection, cursor_send=cursor, commited=True)
                return Response({'status': 'confirm'}, status.HTTP_200_OK)
            else:
                self.__close_connections__(connect=connection, cursor_send=cursor)
                return Response({'status': 'expired'}, status.HTTP_401_UNAUTHORIZED)
        else:
            self.__close_connections__(connect=connection, cursor_send=cursor)
            return Response({'status': 'denied'}, status.HTTP_401_UNAUTHORIZED)

    # Function to get amount of elements from stock
    def get_amount_elements_stock(self) -> Response:

        # Connect to database
        connection: cnt = self.connect_to_db()

        cursor: crs = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM product")

        self.total_elements_stock = cursor.fetchone()[0]

        self.__close_connections__(connect=connection, cursor_send=cursor)

        return ResponseType.SUCCESS.value

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

    # TODO make changes
    def process_purchases(self, data: QueryDict) -> Response:
        client = data.get('client')
        products = data.get('products')

        if not client:
            return Response({'error': 'Please provide the client information',
                             'required_fields:': 'ci, name, email, phone'}, status=status.HTTP_400_BAD_REQUEST)

        if not products:
            return Response({'error': 'Please provide the products to purchase',
                             'required_fields': '[id, quantity]'}, status=status.HTTP_400_BAD_REQUEST)

        # Orden de compra: id, fecha, total, id_cliente
        # Cliente: CI, nombre, email, telefono

        # Price_all_products
        price_all_products_calct = self.__process_total_price_products_purchased__(products).data['total_price']

        connection: cnt = self.connect_to_db()
        cursor: crs = connection.cursor()

        # Agnadir cliente if not exists

        cursor.execute(f"INSERT INTO client (ci, name, email, phone) SELECT '{client['ci']}', "
                       f"'{client['name']}',"
                       f"'{client['email']}', '{client['phone']}' WHERE NOT EXISTS (SELECT 1 FROM client WHERE "
                       f"ci='{client['ci']}')")

        # Orden de compra:
        products = json.dumps(products)
        cursor.execute(f"""
            INSERT INTO purchase_order (date_done, total_amount, id_client, productos_comprados) 
            VALUES ('{now()}', {price_all_products_calct}, '{client['ci']}', '{products}')
        """)

        self.update_purchased_products(data.get('products'), cursor)

        self.__close_connections__(connect=connection, cursor_send=cursor, commited=True)
        return Response({'total_price': price_all_products_calct}, status=status.HTTP_200_OK)

    def __process_total_price_products_purchased__(self, products: list) -> Response:
        connection: cnt = self.connect_to_db()
        cursor: crs = connection.cursor()

        total_price = 0

        for product in products:
            product_id = product['id']
            quantity = product['quantity']

            cursor.execute(f"SELECT price FROM product WHERE id_product={product_id}")
            price = cursor.fetchone()[0]

            total_price += price * quantity

        self.__close_connections__(connect=connection, cursor_send=cursor)

        return Response({'total_price': total_price}, status=status.HTTP_200_OK)

    @staticmethod
    def search_products(self, search_query: str) -> Response:
        query = f"SELECT * FROM product WHERE name LIKE %s"
        elements = Product.objects.raw(query, [f'%{search_query}%'])

        if not elements:
            return ResponseType.NOT_FOUND.value
        else:
            serializer = ProductSerializer(elements, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
