import psycopg2
from .settings import DATABASES
from enum import Enum
from django.contrib.auth.hashers import check_password


# Aquí se declararán las clases y funciones que se encargarán
# de realizar consultas a la base de datos

class ResponseType(Enum):
    # Caso que la operacion se realizó con éxito
    SUCCESS = {
        'status': 'success',
        'code': 200,
        'message': 'Operación realizada con éxito'
    }

    # Caso en que haya dado algun error
    ERROR = {
        'status': 'error',
        'code': 400,
        'message': 'Error en la operacion'
    }

    # Caso que no se encuentre ningun elemento
    NOT_FOUND = {
        'status': 'notfound',
        'code': 404,
        'message': 'Elemento no encontrado'
    }

    # Caso que exista ya un elemento
    EXIST = {
        'status': 'founded',
        'code': 409,
        'message': 'Elemento ya existe'
    }


class CrudDB:
    def __init__(self):
        pass

    # Las funciones se realizarán dependiendo de la tabla que se quiera consultar
    @staticmethod
    def connect_to_db():
        conn = None
        try:
            conn = psycopg2.connect(
                host=DATABASES['default']['HOST'],
                database=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD']
            )
            print('Connected to the database')

        except psycopg2.Error as e:
            print(f'Ocurrio un error: {e}')
            return ResponseType.ERROR.value['code']

        return conn

    # Function to register users
    def register_user(self, username: str, password: str) -> int:
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
        if connection == ResponseType.ERROR.value['code']:
            return ResponseType.ERROR.value['code']
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
                return ResponseType.SUCCESS.value['code']
            else:
                # If the user exists, close the cursor and the connection and return a code indicating that the user
                # already exists
                cursor.close()
                connection.close()
                return ResponseType.EXIST.value['code']

    # Function to log in users
    def log_in_user(self, username: str, password: str) -> int:
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
        if connection == ResponseType.ERROR.value['code']:
            return ResponseType.ERROR.value['code']
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
                return ResponseType.NOT_FOUND.value['code']
            else:
                # If the user exists, retrieve the hashed password of the user from the database
                cursor.execute(f"SELECT password FROM auth_user WHERE username = '{username}'")
                user_password = cursor.fetchone()[0]

                # Use Django's check_password function to compare the provided password with the stored hashed password
                if check_password(password, user_password):
                    # If the passwords match, close the cursor and the connection and return a success code
                    cursor.close()
                    connection.close()
                    return ResponseType.SUCCESS.value['code']
                else:
                    # If the passwords do not match, close the cursor and the connection and return an error code
                    cursor.close()
                    connection.close()
                    return ResponseType.ERROR.value['code']

    def connect_test(self):
        connection = self.connect_to_db()
        print('Conectado, cerrando conexion')
        connection.close()
        return ResponseType.SUCCESS.value['code']
