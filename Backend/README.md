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
The administrative endpoints are for managing the system databases. Offers tools for managing
CRUD actions in the database. <br/>
Administrative endpoints continue with the principle of the general URL, adding an /admin/.<br/>
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

`Returns a JSON with an array of elements that corresponds to objects` `HTTP_200_OK`

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

`Returns a JSON with an array of elements that corresponds to employees` `HTTP_200_OK`

<hr/>

## (POST) Endpoints
### insert_product
This endpoint is responsible for insert a product into the database.

<strong>URL: http://localhost:8000/api/admin/insert_product/</strong>

<b>Required input data: `form-data`</b><br/>

| Key         | Value  | Required |
|-------------|--------|----------|
| name        | String | True     |
| price       | number | True     |
| stock       | number | True     |
| inventory   | number | False    |
| description | String | False    |
| image       | File   | False    |
| category    | String | False    |

If any of the required fields are missing, a JSON will be returned expressing the following:

{'error': 'Please provide all the required fields',
'mandatory_fields': 'name, price, stock',
'optional_fields': 'description, image, category, inventory'} `HTTP_400_BAD_REQUEST`

<strong>Return JSON Example: </strong>

 `Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

# Public/General Endpoints
Public/General endpoints are mainly used to display information to the user.<br/>
Public/General endpoints continue with the principle of the general URL, adding an /public/.<br/>
Example: http://localhost:8000/api/public/.

## (GET) Endpoints
### get_objects
This endpoint is responsible for returning a defined number of products stored in the database, and returning 
two URLS that belong to the website pagination.

<strong>URL: http://localhost:8000/api/public/objects/?page=0</strong><br/>

The information page=# refers to the page that you will find on the web, which is automated by the response
from the api. It starts with page=0.

<strong>Return JSON Example: </strong>

{
    "elements": [
        {
            "id_producto": 1,
            "nombre": "Coca cola",
            "precio": "15.00",
            "stock": 100000,
            "categoria": "Bebidas",
            "imagen": "/media/stock/R_mebF9xG.jpeg",
            "descripcion": "Mejor marca de refresco de cola"
        }
    ],
    "urls": {
        "next": null,
        "previous": null
    }
}

`Returns a JSON with a list of elements that corresponds to the products and two urls that correspond to the following
API call and the previous call, if there is no pagination it returns Null` `HTTP_200_OK`



## (POST) Endpoints
###