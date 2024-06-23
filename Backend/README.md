# EliteStock API 
This API is developed with the purpose of serving information to the Frontend of the website that EliteStock is developed.
It is developed with Django-Rest_Framework with PostgreSQL as a database manager. At a general level this project
It is developed with the objective of meeting the objectives oriented in the final task that corresponds to us in the subject
Database. The choice of technologies was with the objective of expanding our knowledge and improving ourselves as
future programmers.

# Authentication
Authentication is not yet available. The development of it will begin soon.

# Endpoints
All endpoints in this API start with the URL: http://localhost:8000/api/.

There are two types of endpoints at the moment, those that respond to administrative requests and those that respond to requests
general purpose or public purpose.

# Administrative Endpoints
Administrative endpoints continue with the principle of the general URL, adding an /admin/.
Example: http://localhost:8000/api/admin/.

## (GET) Endpoints
### get_all_products
This endpoint is responsible for returning all the products stored in the database.

<strong>URL: http://localhost:8000/api/admin/products/</strong>

<strong>Return JSON Example: </strong>

{
    "elements": [
        {
            "id_producto": 39,
            "nombre": "ASUS Monitor",
            "precio": "400.00",
            "stock": 80,
            "categoria": "Tecnologia",
            "imagen": "/media/stock/_145a3916-d853-4091-a586-168dd8b8a5f8.jpeg",
            "descripcion": "Monitor 240HZ."
        }
    ]
}

`Returns a JSON with an array of elements that corresponds to objects`

<hr/>

### get_all_employees
This endpoint is responsible for returning all the employees stored in the database.

<strong>URL: http://localhost:8000/api/admin/employees/</strong>

<strong>Return JSON Example: </strong>

{
    "elements": [
        {
            "carnet_identidad": "1",
            "nombre": "Juan",
            "salario": "3000.00",
            "id_jefe": null
        }
    ]
}

`Returns a JSON with an array of elements that corresponds to employees`

<hr/>

## (POST) Endpoints
###

# Public/General Endpoints

## (GET) Endpoints
###

## (POST) Endpoints
###