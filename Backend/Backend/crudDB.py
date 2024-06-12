import psycopg2
from .settings import DATABASES

# Aquí se declararán las clases y funciones que se encargarán
# de realizar consultas a la base de datos


class CrudDB:
    def __init__(self):
        pass

    # Las funciones se realizarán dependiendo de la tabla que se quiera consultar
    def connect_to_db_test(self):
        conn = None
        try:
            print(DATABASES['default']['HOST'])
            print(DATABASES['default']['NAME'])
            print(DATABASES['default']['USER'])
            print(DATABASES['default']['PASSWORD'])

            conn = psycopg2.connect(
                host=DATABASES['default']['HOST'],
                database=DATABASES['default']['NAME'],
                user=DATABASES['default']['USER'],
                password=DATABASES['default']['PASSWORD']
            )
            print('Connected to the database')

        except psycopg2.Error as e:
            print(f'Ocurrio un error: {e}')

        return conn


    def register_user(self, username, password):
        connection = self.connect_to_db_test()
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO public.auth_user (username, password) VALUES ('{username}', '{password}')")
        connection.commit()
        cursor.close()
        connection.close()

    def connect_test(self):
        connection = self.connect_to_db_test()
        print('Conectado, cerrando conexion')
        connection.close()
        