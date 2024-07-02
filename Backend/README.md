# Index

- [Presentation](#elitestore-api)
- [Authentication](#authentication)
    - [Register](#register-endpoint-post)
    - [Login](#login-endpoint-post)
    - [Validating](#validate-token-post)
- [Endpoints](#endpoints)
- [Administrative Endpoints](#administrative-endpoints)
    - [(GET) Endpoints](#get-endpoints)
        - [get_all_products](#get_all_products-get)
        - [get_all_employees](#get_all_employees-get)
        - [get_all_sales_reports](#get_all_sales_reports-get)
        - [get_all_inventories](#get_all_inventories-get)
        - [get_all_warehouse](#get_all_warehouses-get)
        - [get_all_messengers](#get_all_messengers-get)
    - [(POST) Endpoints](#post-endpoints)
        - [insert_product](#insert_product-post)
        - [update_product](#update_product-post)
        - [delete_product](#delete_product-post)
        - [delete_products](#delete_products-post)
        - [insert_employee](#insert_employee-post)
        - [update_employee](#update_employee-post)
        - [delete_employee](#delete_employee-post)
        - [insert_inventory](#insert_inventory-post)
        - [delete_inventory](#delete_inventory-post)
        - [insert_warehouse](#insert_warehouse-post)
        - [delete_warehousue](#delete_warehouse-post)
        - [insert_messenger](#insert_messenger-post)
        - [update_messenger](#update_messenger-post)
        - [delete_messenger](#delete_messenger-post)
        - [generate_inventories_reports](#generate_inventories_reports-post)
- [Public/General Endpoints](#publicgeneral-endpoints)
    - [(GET) Endpoints](#get-endpoints-1)
        - [get_objects](#get_objects-get)
    - [(POST) Endpoints](#post-endpoints-1)

# EliteStore API

This API is developed with the purpose of serving information to the Frontend of the website that EliteStore is
developed.
It is developed with Django-Rest_Framework with PostgreSQL as a database manager. At a general level this project
It is developed with the objective of meeting the objectives oriented in the final task that corresponds to us in the
subject
Database. The choice of technologies was with the objective of expanding our knowledge and improving ourselves as
future programmers.

# Authentication

All endpoints in authentication start with the URL: http://localhost:8000/api/auth/.

## Register Endpoint (POST)

The registration endpoint is built on the principle that an Employee can have one Account, only one account.
This registration requires an identity card, a username and password that identifies the account.

<strong>URL: http://localhost:8000/api/auth/register/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key      | Value  | Required |
|----------|--------|----------|
| ci       | string | True     |
| username | string | True     |
| password | string | True     |

`JSON`

```json
{
  "ci": "employee_identifier",
  "username": "username_account",
  "password": "password_account"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide a ci, username and password"
}
```

`HTTP_400_BAD_REQUEST`<br/>

If the CI provided does not correspond to any employee in the database, this error will be returned:

```json
{
  "not_found": "The employee is not registered in the database"
}
```

`HTTP_404_NOT_FOUND`<br/>

If the account is registered by the CI value, the following will be returned:

```json
{
  "error": "Please, this CI is already registered"
}
```

`HTTP_409_CONFLICT`<br/>

If the user is already registered, the following will be returned:

```json
{
  "status": "You cannot register this user because it already exists."
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

```json
{
  "status": "The user has been successfully registered",
  "token": "9827582b7aad21eda5a921011e7b82d40c030faa98c218279c06e0a991f1d278"
}
```

`Returns the registration confirmation status plus the authentication token of the registered user`<br/>
`HTTP_200_OK`<br/>

<hr/>

## Login Endpoint (POST)

The login endpoint is responsible for confirming the input data to perform a successful authentication. This endpoint
will return an authentication token which will be used for internal API calls within the site.

<strong>URL: http://localhost:8000/api/auth/login/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key      | Value  | Required |
|----------|--------|----------|
| username | string | True     |
| password | string | True     |

`JSON`

```json
{
  "username": "username_account",
  "password": "password_account"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide both username and password"
}
```

`HTTP_400_BAD_REQUEST`<br/>

If the user does not exist, a JSON will be returned expressing the following:

```json
{
  "status": "Not_found"
}
```

`HTTP_404_NOT_FOUND`<br/>

If password is incorrect, a JSON will be returned expressing the following:

```json
{
  "status": "Incorrect password"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

```json
{
  "status": "Login successfully",
  "token": "9827582b7aad21eda5a921011e7b82d40c030faa98c218279c06e0a991f1d278"
}
```

`Returns a login confirmation status plus the user's authentication token`<br/>
`HTTP_200_OK`<br/>

<hr/>

## Validate Token (POST)

This endpoint is responsible for validating if the user and token sent are correct and allowing access.

<strong>URL: http://localhost:8000/api/auth/validate/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key        | Value  | Required |
|------------|--------|----------|
| username   | string | True     |
| auth_token | string | True     |

`JSON`

```json
{
  "username": "username_account",
  "auth_token": "auth_token archived in user cache"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "status": "denied"
}
```

`HTTP_401_UNAUTHORIZED`<br/>

If the username provided is not registered, a JSON will be returned expressing the following:

```json
{
  "status": "denied"
}
```

`HTTP_401_UNAUTHORIZED`<br/>

If the supplied token is not the same as the one stored in the user, a JSON will be returned expressing the following:

```json
{
  "status": "denied"
}
```

`HTTP_401_UNAUTHORIZED`<br/>

If the token is expired, a JSON will be returned expressing the following:

```json
{
  "status": "expired"
}
```

`HTTP_401_UNAUTHORIZED`<br/>

<strong>Return JSON Example: </strong>

```json
{
  "status": "confirm"
}
```

`Returns the confirmation`<br/>
`HTTP_200_OK`<br/>

# Endpoints

All endpoints in this API start with the URL: http://localhost:8000/api/.

There are two types of endpoints at the moment, those that respond to administrative requests and those that respond to
requests
general purpose or public purpose.

# Administrative Endpoints

The administrative endpoints are for managing the system databases. Offers tools for managing
CRUD actions in the database. <br/>
Administrative endpoints continue with the principle of the general URL, adding an /admin/.<br/>
Example: http://localhost:8000/api/admin/.

## (GET) Endpoints

### get_all_products (GET)

This endpoint is responsible for returning all the products stored in the database.

<strong>URL: http://localhost:8000/api/admin/products/</strong>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id_product": 8,
      "name": "Fanta",
      "price": "15.00",
      "stock": 100000,
      "category": "Bebidas",
      "image": "/media/stock/OIP_IalOJN6.jpeg",
      "description": "Descripcion de prueba",
      "id_inventory": 1
    }
  ]
}
```

`Returns a JSON with an array of elements that corresponds to objects` `HTTP_200_OK`

<hr/>

### get_all_employees (GET)

This endpoint is responsible for returning all the employees stored in the database.

<strong>URL: http://localhost:8000/api/admin/employees/</strong>

<strong>Return JSON Example: </strong>

```json
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
```

`Returns a JSON with an array of elements that corresponds to employees` `HTTP_200_OK`

<hr/>

### get_all_inventories (GET)

This endpoint is responsible for returning all the inventories stored in database.

<strong>URL: http://localhost:8000/api/admin/inventories/</strong>

<strong>_Errors JSON Examples:_</strong>

En caso que no existan inventarios en la base de datos retorna:

```json
{
  "error": "is empty"
}
```

`HTTP_404_NOT_FOUND`<br/>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id_inventario": 3,
      "categoria": "Bebidas",
      "id_almacen": 1
    }
  ]
}
```

<hr/>

### get_all_sales_reports (GET)

This endpoint is responsible for returning all the sales reports stored in the database.

<strong>URL: http://localhost:8000/api/admin/sales_reports/</strong>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id": 2,
      "date_time_delivery": "2024-06-29T14:26:27.799085Z",
      "total_amount": "400.00",
      "id_purchase_order": 2,
      "messenger": "03112366746"
    }
  ]
}
```

`Returns a JSON with an array of elements that corresponds to reports` `HTTP_200_OK`

<hr/>

### get_all_inventory_reports (GET)

This endpoint is responsible for returning all the inventory reports stored in the database.

<strong>URL: http://localhost:8000/api/admin/inventory_reports/</strong>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id": 2,
      "stock_amount": 30,
      "total_value": "3000.00",
      "id_inventory": 2
    }
  ]
}
```

`Returns a JSON with an array of elements that corresponds to inventories` `HTTP_200_OK`

<hr/>

### get_all_warehouses (GET)

This endpoint is responsible for returning all the warehouses stored in the database.

<strong>URL: http://localhost:8000/api/admin/warehouses/</strong>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id_warehouse": 2,
      "name": "EliteStore",
      "location": "UCI"
    }
  ]
}
```

`Returns a JSON with an array of elements that corresponds to warehouses` `HTTP_200_OK`

<hr/>

### get_all_messengers (GET)

This endpoint is responsible for returning all messengers stored in the database.

<strong>URL: http://localhost:8000/api/admin/messengers/</strong>

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "ci": "03112366746",
      "vehicle": "carro",
      "salary_per_km": "30.00"
    }
  ]
}
```

`Returns a JSON with an array of elements that corresponds to messengers` `HTTP_200_OK`

<hr/>

## (POST) Endpoints

### insert_product (POST)

This endpoint is responsible for insert a product into the database.

<strong>URL: http://localhost:8000/api/admin/insert_product/</strong>

<b>Required input data: `form-data`</b><br/>

| Key          | Value  | Required |
|--------------|--------|----------|
| name         | String | True     |
| price        | number | True     |
| stock        | number | True     |
| id_inventory | number | False    |
| description  | String | True     |
| image        | File   | False    |
| category     | String | False    |

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "name, price, stock, description",
  "optional_fields": "image, category, inventory"
} 
```

`HTTP_400_BAD_REQUEST` <br/>

If the inventory that is entered does not exist, a JSON will be returned expressing the following:

```json
{
  "error": "The inventory you are entering does not exist",
  "code": "23503"
}
```

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

<!-- Needs Review -->

### update_product (POST)

This endpoint is responsible for update a product that exists in the database.

<strong>URL: http://localhost:8000/api/admin/insert_product/</strong>

<b>Required input data: `form-data`</b><br/>

| Key         | Value  | Required |
|-------------|--------|----------|
| name        | String | True     |
| price       | number | True     |
| stock       | number | True     |
| inventory   | number | True     |
| description | String | False    |
| image       | File   | False    |
| category    | String | True?    |
| entry_data  | Date   | True     |

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "name, price, stock, category, inventory, entry_date, inventory",
  "optional_fields": "description, image"
} 
```

`HTTP_400_BAD_REQUEST` <br/>

_In any case, the filling out of this form will be automated by an autofill of fields in the frontend._

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_product (POST)

This endpoint is responsible for delete a product that exists in the database.

<strong>URL: http://localhost:8000/api/admin/delete_product/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key | Value  | Required |
|-----|--------|----------|
| id  | number | True     |

`JSON:`

```json
{
  "id": "number_value"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide an id of product you will delete"
}
```

`HTTP_400_BAD_REQUEST`

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_products (POST)

This endpoint has the same objective as the endpoint of deleting a product, unlike this endpoint deleting multiple
products.
from an array of integers.

<strong>URL: http://localhost:8000/api/admin/delete_products/</strong>

<b>Required input data: `JSON`</b>

`JSON: `

```json
{
  "elements": [
    "Array of integer. There are no restrictions with other values, the API will ignore them"
  ]
}
```

`Required field: elements`

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide elements to delete"
}
```

`HTTP_400_BAD_REQUEST`

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### insert_employee (POST)

This endpoint is responsible for insert an employee into the database.

<strong>URL: http://localhost:8000/api/admin/insert_employee/</strong>

<b>Required input data: `JSON`</b>

```json
{
  "employee": {
    "ci": "Identity card, identifier",
    "name": "String",
    "salary": "number",
    "id_boss": "Identify of another employee"
  }
}
```

`Required fields:` `employee`, `CI`, `name`, `salary`.

If any of the required fields are missing, a JSON will be returned expressing the following:

In case the employee is missing:

```json
{
  "error": "Please prove information about employee"
}
```

In case any of the other required fields are missing:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "ci, name, salary",
  "optional_fields": "id_boss"
}
```

`HTTP_400_BAD_REQUEST`<br/>

Another error that could occur is that you may be trying to insert an employee that already exists in the database.

```json
{
  "error": "The CI you are entering already exists in the database",
  "code": "23505"
}
```

`HTTP_409_CONFLICT`<br/>

Another error that can occur is if the boss_id does not correspond to any other employee in the database.

```json
{
  "error": "The employee to whom the id_boss corresponds does not exist",
  "code": "23503"
}
```

`HTTP_409_CONFLICT`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### update_employee (POST)

This endpoint is responsible for update an employee in the database.

<strong>URL: http://localhost:8000/api/admin/update_employee/</strong>

<b>Required input data: `JSON`</b><br/>

```json
{
  "employee": {
    "CI": "Identity card, identifier",
    "name": "String",
    "salary": "number",
    "boss": "Identify of another employee"
  }
}
```

`Required fields:` `employee`, `CI`, `name`, `salary`, `boss`.

In case the employee is missing:

```json
{
  "error": "Please prove information about employee"
}
```

In case any of the other required fields are missing:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "CI, name, salary, boss"
}
```

`HTTP_400_BAD_REQUEST`<br/>

_In any case, the filling out of this form will be automated by an autofill of fields in the frontend._

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_employee (POST)

This endpoint is responsible for delete an employee that exists in the database.
<strong>URL: http://localhost:8000/api/admin/delete_employee/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key | Value  | Required |
|-----|--------|----------|
| ci  | String | True     |

`JSON:`

```json
{
  "ci": "employee_indentify"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please prove a ci to delete"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### insert_inventory (POST)

This endpoint is responsible for insert an employee into the database.

<strong>URL: http://localhost:8000/api/admin/insert_inventory/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key        | Value  | Required |
|------------|--------|----------|
| category   | String | True     |
| storage_id | Number | True     |

`JSON`

```json
{
  "category": "String_example",
  "storage_id": 30
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide a category and a storage_id"
}
```

`HTTP_400_BAD_REQUEST`<br/>

In case there is no valid warehouse, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide a valid warehouse"
}
```

`HTTP_404_NOT_FOUND`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_inventory (POST)

This endpoint is responsible for delete an inventory that exists in the database.

<strong>URL: http://localhost:8000/api/admin/delete_inventory/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key | Value  | Required |
|-----|--------|----------|
| id  | Number | True     |

`JSON:`

```json
{
  "id": 1
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide an id"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### insert_warehouse (POST)

This endpoint is responsible for insert a warehouse into the database.

<strong>URL: http://localhost:8000/api/admin/insert_warehouse/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key      | Value  | Required |
|----------|--------|----------|
| name     | String | True     |
| location | String | True     |

`JSON`

```json
{
  "name": "String_example",
  "location": "Location example"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "name, location"
}
```

`HTTP_400_BAD_REQUEST`<br/>

In case the warehouse already exists, a JSON will be returned expressing the following:

```json
{
  "error": "There is already a warehouse with this name"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_warehouse (POST)

This endpoint is responsible for delete a warehouse that exists in the database.
<b>REQUIRE REVIEW</b>

<strong>URL: http://localhost:8000/api/admin/delete_warehouse/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key          | Value  | Required |
|--------------|--------|----------|
| id_warehouse | Number | True     |

`JSON:`

```json
{
  "id_warehouse": 1
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide an id to delete warehouse"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### insert_messenger (POST)

This endpoint is responsible for insert a messenger into the database.

<strong>URL: http://localhost:8000/api/admin/insert_messenger/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data`

| Key           | Value  | Required |
|---------------|--------|----------|
| employee_ci   | String | True     |
| vehicle       | String | True     |
| salary_per_km | Number | True     |

`JSON`

```json
{
  "employee_ci": "Existing employee identifier",
  "vehicle": "String Example",
  "salary_per_km": 30
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide all the required fields",
  "mandatory_fields": "employee_id, vehicle, salary_per_km"
}
```

`HTTP_400_BAD_REQUEST`<br/>

In the event that there is no employee with the CI, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide a CI that belongs to an employee"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### update_messenger (POST)

This endpoint is responsible for update a messenger in the database.

<strong>URL: http://localhost:8000/api/admin/update_messenger/</strong>

<b>Required input data: `form-data` or `JSON`</b><br/>

`form-data`

| Key           | Value  | Required |
|---------------|--------|----------|
| employee_ci   | String | True     |
| vehicle       | String | True     |
| salary_per_km | number | True     |

`JSON`

```json
{
  "employee_ci": "Existing employee identifier",
  "vehicle": "String Example",
  "salary_per_km": 30
}
```

`HTTP_400_BAD_REQUEST`<br/>

_In any case, the filling out of this form will be automated by an autofill of fields in the frontend._

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### delete_messenger (POST)

This endpoint is responsible for delete a messenger that exists in the database.

<strong>URL: http://localhost:8000/api/admin/delete_messenger/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key | Value  | Required |
|-----|--------|----------|
| ci  | String | True     |

`JSON:`

```json
{
  "ci": "CI example"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please prove a ci to delete messenger"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

### generate_inventories_reports (POST)

This endpoint is responsible for generating reports on all inventories in the database.

<strong>URL: http://localhost:8000/api/admin/generate_invetories_reports/</strong>

<b>Required input data: `form-data` or `JSON`</b>

`form-data:`

| Key         | Value  | Required |
|-------------|--------|----------|
| ci_employee | String | True     |

`JSON:`

```json
{
  "ci_employee": "Ci of the employee who is logged in"
}
```

If any of the required fields are missing, a JSON will be returned expressing the following:

```json
{
  "error": "Please provide an ci_employee"
}
```

`HTTP_400_BAD_REQUEST`<br/>

In case you have already made a report on the day, a JSON will be returned expressing the following:

```json
{
  "error": "You have already made the corresponding inventory reports on the day",
  "status": "not_today",
  "last_date": "YYYY-MM-DD"
}
```

`HTTP_400_BAD_REQUEST`<br/>

<strong>Return JSON Example: </strong>

`Returns confirmation of the process -> {'status': 'Success'}` `HTTP_200_OK`

<hr/>

# Public/General Endpoints

Public/General endpoints are mainly used to display information to the user.<br/>
Public/General endpoints continue with the principle of the general URL, adding an /public/.<br/>
Example: http://localhost:8000/api/public/.

## (GET) Endpoints

### get_objects (GET)

This endpoint is responsible for returning a defined number of products stored in the database, and returning
two URLS that belong to the website pagination.

<strong>URL: http://localhost:8000/api/public/objects/?page=0</strong><br/>

The information page=# refers to the page that you will find on the web, which is automated by the response
from the api. It starts with page=0.

<strong>Return JSON Example: </strong>

```json
{
  "elements": [
    {
      "id_product": 1,
      "name": "Coca cola",
      "price": "15.00",
      "stock": 100000,
      "category": "Bebidas",
      "image": "/media/stock/R_mebF9xG.jpeg",
      "description": "Mejor marca de refresco de cola"
    }
  ],
  "urls": {
    "next": null,
    "previous": null
  }
}
```

`Returns a JSON with a list of elements that corresponds to the products and two urls that correspond to the following
API call and the previous call, if there is no pagination it returns Null` `HTTP_200_OK`

## (POST) Endpoints

###